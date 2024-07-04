from flask import Flask, redirect, request, render_template, flash
from surveys import satisfaction_survey

app = Flask(__name__)
app.secret_key = "asupersecretpassword1"

responses = []
TOTAL_QUESTIONS = len(satisfaction_survey.questions)

current_question = 0
@app.route("/")
def index():
    global current_question
    current_question = 0
    return render_template("home.html", survey_title=satisfaction_survey.title)

@app.route("/questions")
def questions_redirect():
    return redirect("/questions/0")

@app.route("/questions/<int:num>")
def questions_page(num):
    if num != current_question:
        flash("You are accessing an invalid portion of the survey.")
        return redirect(f'/questions/{current_question}')
    question = satisfaction_survey.questions[num].question
    choices  = satisfaction_survey.questions[num].choices

    return render_template("questions.html", question=question, choices=choices)

@app.route("/answer", methods=["POST", "GET"])
def answer():
    global current_question
    if current_question != -1:
        responses.append(request.form['ans'])
    current_question += 1
    if current_question >= TOTAL_QUESTIONS:
        return redirect('/thanks')
    return redirect(f'/questions/{current_question}')

@app.route("/thanks")
def thanks():
    return "<h1>Thank You</h1>"