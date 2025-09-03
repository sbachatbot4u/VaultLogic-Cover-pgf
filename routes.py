from flask import render_template, request, jsonify, flash, redirect, url_for
from app import app
from forms import DemoRequestForm, ChatForm
from compliance_data import search_handbook, PREDEFINED_QA, COMPLIANCE_HANDBOOK
import logging

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/security')
def security():
    return render_template('security.html')

@app.route('/demo')
def demo():
    chat_form = ChatForm()
    return render_template('demo.html', 
                         chat_form=chat_form, 
                         predefined_questions=PREDEFINED_QA,
                         handbook_sections=COMPLIANCE_HANDBOOK["sections"])

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = DemoRequestForm()
    
    if form.validate_on_submit():
        # Log the demo request (in production, this would be saved to database or sent via email)
        logging.info(f"Demo request received: {form.first_name.data} {form.last_name.data} from {form.company.data}")
        flash('Thank you for your demo request! Our team will contact you within 24 hours.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html', form=form)

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat questions about the compliance handbook"""
    chat_form = ChatForm()
    
    if chat_form.validate_on_submit():
        question = chat_form.question.data
        
        # Search for answers in the compliance handbook
        results = search_handbook(question)
        
        if results:
            result = results[0]
            return jsonify({
                'success': True,
                'question': question,
                'answer': result.answer,
                'sources': result.sources or []
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No relevant information found.'
            })
    
    return jsonify({
        'success': False,
        'error': 'Invalid question format.'
    })

@app.route('/api/predefined-question')
def get_predefined_question():
    """Get a random predefined question for demo purposes"""
    import random
    question = random.choice(PREDEFINED_QA)
    return jsonify({
        'question': question.question,
        'answer': question.answer,
        'sources': question.sources
    })

@app.errorhandler(404)
def not_found_error(error):
    return render_template('base.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('base.html'), 500
