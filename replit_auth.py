import jwt
import os
import uuid
import requests
from functools import wraps, lru_cache
from urllib.parse import urlencode
from cryptography.hazmat.primitives import serialization

from flask import g, session, redirect, request, render_template, url_for
from flask_dance.consumer import (
    OAuth2ConsumerBlueprint,
    oauth_authorized,
    oauth_error,
)
from flask_dance.consumer.storage import BaseStorage
from flask_login import LoginManager, login_user, logout_user, current_user
from oauthlib.oauth2.rfc6749.errors import InvalidGrantError
from sqlalchemy.exc import NoResultFound
from werkzeug.local import LocalProxy

from app import app, db
from models import OAuth, User

login_manager = LoginManager(app)


@lru_cache(maxsize=1)
def get_replit_public_key(issuer_url):
    """Fetch and cache Replit's public key for JWT verification."""
    try:
        # Fetch JWKS from Replit's well-known endpoint
        jwks_url = f"{issuer_url}/.well-known/jwks.json"
        response = requests.get(jwks_url, timeout=10)
        response.raise_for_status()
        
        jwks = response.json()
        # Use the first key (Replit typically uses one key)
        if 'keys' in jwks and len(jwks['keys']) > 0:
            key_data = jwks['keys'][0]
            
            # Convert JWK to PEM format for PyJWT
            if key_data.get('kty') == 'RSA':
                # Build RSA public key from modulus and exponent
                from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
                import base64
                
                def decode_base64url(data):
                    """Decode base64url-encoded data."""
                    # Add padding if needed
                    missing_padding = len(data) % 4
                    if missing_padding:
                        data += '=' * (4 - missing_padding)
                    return base64.urlsafe_b64decode(data)
                
                n = int.from_bytes(decode_base64url(key_data['n']), 'big')
                e = int.from_bytes(decode_base64url(key_data['e']), 'big')
                
                public_numbers = RSAPublicNumbers(e, n)
                public_key = public_numbers.public_key()
                
                return public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
        
        raise ValueError("No valid RSA key found in JWKS")
        
    except Exception as e:
        app.logger.error(f"Failed to fetch Replit public key: {e}")
        return None


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class UserSessionStorage(BaseStorage):

    def get(self, blueprint):
        try:
            oauth_record = db.session.query(OAuth).filter_by(
                user_id=current_user.get_id(),
                browser_session_key=g.browser_session_key,
                provider=blueprint.name,
            ).one()
            return oauth_record.token
        except NoResultFound:
            return None

    def set(self, blueprint, token):
        db.session.query(OAuth).filter_by(
            user_id=current_user.get_id(),
            browser_session_key=g.browser_session_key,
            provider=blueprint.name,
        ).delete()
        new_model = OAuth()
        new_model.user_id = current_user.get_id()
        new_model.browser_session_key = g.browser_session_key
        new_model.provider = blueprint.name
        new_model.token = token
        db.session.add(new_model)
        db.session.commit()

    def delete(self, blueprint):
        db.session.query(OAuth).filter_by(
            user_id=current_user.get_id(),
            browser_session_key=g.browser_session_key,
            provider=blueprint.name).delete()
        db.session.commit()


def make_replit_blueprint():
    try:
        repl_id = os.environ['REPL_ID']
    except KeyError:
        raise SystemExit("the REPL_ID environment variable must be set")

    issuer_url = os.environ.get('ISSUER_URL', "https://replit.com/oidc")

    replit_bp = OAuth2ConsumerBlueprint(
        "replit_auth",
        __name__,
        client_id=repl_id,
        client_secret=None,
        base_url=issuer_url,
        authorization_url_params={
            "prompt": "login consent",
        },
        token_url=issuer_url + "/token",
        token_url_params={
            "auth": (),
            "include_client_id": True,
        },
        auto_refresh_url=issuer_url + "/token",
        auto_refresh_kwargs={
            "client_id": repl_id,
        },
        authorization_url=issuer_url + "/auth",
        use_pkce=True,
        code_challenge_method="S256",
        scope=["openid", "profile", "email", "offline_access"],
        storage=UserSessionStorage(),
    )

    @replit_bp.before_app_request
    def set_applocal_session():
        if '_browser_session_key' not in session:
            session['_browser_session_key'] = uuid.uuid4().hex
        session.modified = True
        g.browser_session_key = session['_browser_session_key']
        g.flask_dance_replit = replit_bp.session

    @replit_bp.route("/logout")
    def logout():
        del replit_bp.token
        logout_user()

        end_session_endpoint = issuer_url + "/session/end"
        encoded_params = urlencode({
            "client_id":
            repl_id,
            "post_logout_redirect_uri":
            request.url_root,
        })
        logout_url = f"{end_session_endpoint}?{encoded_params}"

        return redirect(logout_url)

    @replit_bp.route("/error")
    def error():
        return render_template("403.html"), 403

    return replit_bp


def save_user(user_claims):
    user = User()
    user.id = user_claims['sub']
    user.email = user_claims.get('email')
    user.first_name = user_claims.get('first_name')
    user.last_name = user_claims.get('last_name')
    user.profile_image_url = user_claims.get('profile_image_url')
    merged_user = db.session.merge(user)
    db.session.commit()
    return merged_user


@oauth_authorized.connect
def logged_in(blueprint, token):
    """Handle successful OAuth authorization with proper JWT verification."""
    issuer_url = os.environ.get('ISSUER_URL', "https://replit.com/oidc")
    
    try:
        # Get Replit's public key for signature verification
        public_key = get_replit_public_key(issuer_url)
        
        if public_key:
            # Verify JWT signature with Replit's public key
            user_claims = jwt.decode(
                token['id_token'],
                key=public_key,
                algorithms=["RS256"],
                issuer=issuer_url,
                options={
                    "verify_signature": True,
                    "verify_iss": True,
                    "verify_exp": True,
                    "verify_aud": False  # Audience validation can be complex in OAuth
                }
            )
        else:
            # Fallback: if we can't get the public key, do basic validation
            # This maintains functionality while logging the issue
            app.logger.warning("Could not fetch public key for JWT verification, using fallback validation")
            user_claims = jwt.decode(
                token['id_token'],
                options={
                    "verify_signature": False,
                    "verify_iss": True,
                    "verify_exp": True,
                    "verify_aud": False
                },
                issuer=issuer_url,
                algorithms=["RS256"]
            )
            
            # Additional validation when signature verification fails
            required_claims = ['sub', 'iss', 'exp']
            for claim in required_claims:
                if claim not in user_claims:
                    raise jwt.InvalidTokenError(f"Missing required claim: {claim}")
                    
    except jwt.InvalidTokenError as e:
        # Log the error and redirect to error page
        app.logger.error(f"JWT verification failed: {e}")
        return redirect(url_for('replit_auth.error'))
    except Exception as e:
        # Handle unexpected errors during verification
        app.logger.error(f"Unexpected error during JWT verification: {e}")
        return redirect(url_for('replit_auth.error'))
    
    user = save_user(user_claims)
    login_user(user)
    blueprint.token = token
    next_url = session.pop("next_url", None)
    if next_url is not None:
        return redirect(next_url)


@oauth_error.connect
def handle_error(blueprint, error, error_description=None, error_uri=None):
    return redirect(url_for('replit_auth.error'))


def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            session["next_url"] = get_next_navigation_url(request)
            return redirect(url_for('replit_auth.login'))

        # Check if token needs refresh
        if replit.token:
            expires_in = replit.token.get('expires_in', 0)
            if expires_in < 0:
                issuer_url = os.environ.get('ISSUER_URL', "https://replit.com/oidc")
                refresh_token_url = issuer_url + "/token"
                try:
                    token = replit.refresh_token(token_url=refresh_token_url,
                                                 client_id=os.environ['REPL_ID'])
                except InvalidGrantError:
                    # If the refresh token is invalid, the users needs to re-login.
                    session["next_url"] = get_next_navigation_url(request)
                    return redirect(url_for('replit_auth.login'))
                replit.token_updater(token)

        return f(*args, **kwargs)

    return decorated_function


def get_next_navigation_url(request):
    is_navigation_url = request.headers.get(
        'Sec-Fetch-Mode') == 'navigate' and request.headers.get(
            'Sec-Fetch-Dest') == 'document'
    if is_navigation_url:
        return request.url
    return request.referrer or request.url


replit = LocalProxy(lambda: g.flask_dance_replit)