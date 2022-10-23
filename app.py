from flask import Flask, request, render_template,  redirect, flash,  jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from flask import session, make_response
from surveys import *


app = Flask(__name__)

app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

RESPONSES = 'responses'

title = satisfaction_survey.title
instructions = satisfaction_survey.instructions
questions = satisfaction_survey.questions


@app.route('/')
def home_page():
    """Shows home page"""

    if not session[RESPONSES] or len(session[RESPONSES]) == 4:
        return render_template('home.html', title=title,
                               instructions=instructions)
    else:
        flash('You are trying to access an invalid question')
        return redirect(f'/questions/{(len(session[RESPONSES]))}')


@app.route('/survey-session', methods=["POST"])
def prep_session():
    """set session['responses'] to an empty list"""
    if session[RESPONSES]:
        session.clear()
    session[RESPONSES] = []

    return redirect('/questions/0')


@app.route('/questions/<int:q_number>')
def survey_page(q_number):
    """Shows survey questions"""

    if q_number != len(session[RESPONSES]) or len(session[RESPONSES]) == 4:
        if len(session[RESPONSES]) == 4:
            return redirect('/thanks')
        flash('You are trying to access an invalid question')
        return redirect(f'/questions/{len(session[RESPONSES])}')

    question = questions[(q_number)]
    return render_template('questions.html', title=title,
                           instructions=instructions, question=question)


@app.route('/questions/answer', methods=["POST"])
def add_answer():
    """handles survey question post, redirects user to either
        next quesion or the thank-you page"""

    if request.form.get('choice'):

        answer = request.form.get('choice')
        add_to_session = session[RESPONSES]
        add_to_session.append(answer)
        session[RESPONSES] = add_to_session
        q_number = len(session[RESPONSES])

        if len(session[RESPONSES]) == len(questions):
            return redirect('/thanks')

    else:
        flash('Select an option')
        q_number = len(session[RESPONSES])

    return redirect(f'/questions/{q_number}')


@app.route('/thanks')
def thank_you_page():
    """Shows thank you page after survey"""

    if len(session[RESPONSES]) != 4:
        flash('You are trying to access an invalid question')
        return redirect(f'/questions/{len(session[RESPONSES])}')

    return render_template('thanks.html')
