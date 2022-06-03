from flask import Flask, request , render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES_KEY = 'responses'

app = Flask(__name__)

app.debug = True
app.config['SECRET_KEY'] = '<replace with a secret key>'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

@app.route("/")
def show_pick_survey_form():
    """Show pick-a-survey form"""

    return render_template("pick-survey.html", surveys=surveys)


@app.route("/",methods=["POST"])
"""Selects survey"""
def pick_survey():
    survey_id =  request.form['survey_code']

    if request.cookies.get(f"completed_{survey_id}"):
        return render_template("already-done.html")

        survey = surveys[survey_id]
        session[CURRENT_SURVEY_KEY] = survey_id
        return render_template("survey_start.html", survey=survey)

@app.route("/")
def show_survey_start():
    """Select a survey"""

    return render_template('survey_start.html',survey=survey)

@app.route('/begin', methods=["POST"])
def start_survey():
    """Clear the session of responses."""

    session[RESPONSES_KEY] = []

    return redirect("/questions/0")

@app.route("/answer" , methods = ["POST"])
def handle_question():
    """Save response and redirect to next question."""

choice = request.form['answer']

response = session['RESPONSE_KEY']
responses.append(choice)
session[RESPONSE_KEY] = responses

if (len(responses) == len(survey.questions)):
    return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/questions/<int:qid>")
def show_question(qid):
    """Display current question"""
    responses = session.get(RESPONSE_KEY)

    if (responses is None):
        return redirect("/")

    if (len(responses) == len(survey.questions)):

        return redirect("/complete")

    if (len(responses) != qid):

        flash(f"Invalid question id: {qid}. ")
        return redirect(f"/questions/ {len(responses)} ")

    question = survey.questions[qid]
    return render_template("question.html",question_num=qid, question=question)

@app.route("/complete")
def complete():
    """Survey Complete"""

    return render_template("completion.html")