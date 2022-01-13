import copy
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app, session
from flask_login import login_required, current_user
from sqlalchemy import desc
from forum.forms import ForumForm
from models import Forum, Comments, db, Quiz, User, Results
from quiz.forms import QuizForm

quiz_blueprint = Blueprint('quiz', __name__, template_folder='templates')


@quiz_blueprint.route('/quiz')
@login_required
def quiz():
    questions = Quiz.query.all()
    completed = Results.query.filter_by(user_id=current_user.id)
    return render_template('quiz.html', questions=questions, completed=completed)


@quiz_blueprint.route('/quiz_home')
@login_required
def quiz_home():
    session['result'] = ""
    session['completed'] = ""
    return render_template('quiz_home.html')


@quiz_blueprint.route('/quiz', methods=["POST"])
def submit():
    question_id = request.form.get('question_id')
    user_answer = request.form.get('answer')
    question = Quiz.query.filter_by(question_id=question_id).first()

    if int(user_answer) == question.answer:
        new_result = Results(user_id=current_user.id, question_id=question_id)

        db.session.add(new_result)
        db.session.commit()

    completed = Results.query.filter_by(user_id=current_user.id)
    questions = Quiz.query.all()

    return render_template('quiz.html', questions=questions, completed=completed)


@quiz_blueprint.route('/create_question', methods=('GET', 'POST'))
def create_question():
    form = QuizForm()

    if form.validate_on_submit():
        new_question = Quiz(question=form.question.data, option1=form.option1.data, option2=form.option2.data,
                            option3=form.option3.data, option4=form.option4.data, answer=form.answer.data)

        db.session.add(new_question)
        db.session.commit()

        return quiz()
    return render_template('create_quiz_q.html', form=form)
