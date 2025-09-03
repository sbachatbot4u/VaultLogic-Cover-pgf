from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, EmailField
from wtforms.validators import DataRequired, Email, Length

class DemoRequestForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = EmailField('Business Email', validators=[DataRequired(), Email()])
    company = StringField('Company', validators=[DataRequired(), Length(min=2, max=100)])
    company_size = SelectField('Company Size', choices=[
        ('', 'Select company size'),
        ('1-10', '1-10 employees'),
        ('11-50', '11-50 employees'),
        ('51-200', '51-200 employees'),
        ('201-1000', '201-1000 employees'),
        ('1000+', '1000+ employees')
    ], validators=[DataRequired()])
    message = TextAreaField('How can we help you?', validators=[Length(max=500)])

class ChatForm(FlaskForm):
    question = StringField('Ask a question', validators=[DataRequired(), Length(min=5, max=500)])
