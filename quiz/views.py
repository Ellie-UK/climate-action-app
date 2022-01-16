import copy
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app, session
from flask_login import login_required, current_user
from sqlalchemy import desc, func
from forum.forms import ForumForm
from models import Forum, Comments, db, Quiz, User, Results
from quiz.forms import QuizForm

quiz_blueprint = Blueprint('quiz', __name__, template_folder='templates')


@quiz_blueprint.route('/quiz', methods=["GET"])
@login_required
def quiz():
    questions = Quiz.query.all()
    completed = Results.query.filter_by(user_id=current_user.id)
    uncompleted = Quiz.query.all()
    for x in completed:
        for y in questions:
            if x.question_id == y.question_id:
                uncompleted.remove(y)
    if len(uncompleted) == 0:
        correct = Results.query.filter_by(user_id=current_user.id, correct=True).count()
        question_length = len(questions)
        txt = str(correct) + '/' + str(question_length)
    else:
        txt = 'Quiz not completed'
    return render_template('quiz.html', questions=questions, uncompleted=uncompleted, result=txt)


@quiz_blueprint.route('/quiz_home')
@login_required
def quiz_home():
    session['result'] = ""
    session['completed'] = ""
    uncompleted()
    questions = Quiz.query.all()
    if len(uncompleted()) == 0:
        correct = Results.query.filter_by(user_id=current_user.id, correct=True).count()
        question_length = len(questions)
        txt = str(correct) + '/' + str(question_length)
        flag = True
    else:
        txt = 'Quiz not completed'
        flag = False

    return render_template('quiz_home.html', flag=flag, txt=txt)


@quiz_blueprint.route('/quiz', methods=["POST"])
def submit():
    question_id = request.form.get('question_id')
    user_answer = request.form.get('answer')
    question = Quiz.query.filter_by(question_id=question_id).first()

    if int(user_answer) == question.answer:
        new_result = Results(user_id=current_user.id, question_id=question_id, correct=True)
        db.session.add(new_result)
        db.session.commit()

    else:
        new_result = Results(user_id=current_user.id, question_id=question_id, correct=False)
        db.session.add(new_result)
        db.session.commit()

        questions = Quiz.query.all()
        uncompleted()

    return render_template('quiz.html', questions=questions, uncompleted=uncompleted)


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


@quiz_blueprint.route('/delete_quiz')
def delete_quiz():
    Results.query.delete()
    Quiz.query.delete()
    db.session.commit()

    return quiz()


@quiz_blueprint.route('/finish_quiz', methods=('GET', 'POST'))
def finish_quiz():
    correct = Results.query.filter_by(user_id=current_user.id, correct=True).count()
    User.query.filter_by(id=current_user.id).update({"weekly_score": correct})

    if current_user.total_score is None:
        User.query.filter_by(id=current_user.id).update({"total_score": correct})
    else:
        total_score = int(current_user.total_score) + correct
        User.query.filter_by(id=current_user.id).update({"total_score": total_score})

    db.session.commit()


def uncompleted():
    completed = Results.query.filter_by(user_id=current_user.id)
    questions = Quiz.query.all()
    uncompleted = Quiz.query.all()
    for x in completed:
        for y in questions:
            if x.question_id == y.question_id:
                uncompleted.remove(y)

    return uncompleted


@quiz_blueprint.route('/<int:question_id>/update_question', methods=('GET', 'POST'))
def update_question(question_id):
    question = Quiz.query.filter_by(question_id=question_id).first()
    if not question:
        return render_template('500.html')

    form = QuizForm()

    if form.validate_on_submit():
        Quiz.query.filter_by(question_id=question_id).update({"question": form.question.data})
        Quiz.query.filter_by(question_id=question_id).update({"option1": form.option1.data})
        Quiz.query.filter_by(question_id=question_id).update({"option2": form.option2.data})
        Quiz.query.filter_by(question_id=question_id).update({"option3": form.option3.data})
        Quiz.query.filter_by(question_id=question_id).update({"option4": form.option4.data})
        Quiz.query.filter_by(question_id=question_id).update({"answer": form.answer.data})

        db.session.commit()

        return quiz()

    # creates a copy of question object which is independent of database.
    question_copy = copy.deepcopy(question)

    # set update form with title and body of copied post object
    form.question.data = question_copy.question
    form.option1.data = question_copy.option1
    form.option2.data = question_copy.option2
    form.option3.data = question_copy.option3
    form.option4.data = question_copy.option4
    form.answer.data = question_copy.answer

    return render_template('update_question.html', form=form)
