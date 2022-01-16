import copy
from faq.forms import FAQFormQuestion, FAQFormAnswer
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required
from models import FAQ, db

faq_blueprint = Blueprint('faq', __name__, template_folder='templates')


@faq_blueprint.route('/faq')
@login_required
def faq():
    questions = FAQ.query.all()
    return render_template('faq.html', questions=questions)


@faq_blueprint.route('/question', methods=('GET', 'POST'))
def write_question():
    form = FAQFormQuestion()

    if form.validate_on_submit():
        new_question = FAQ(question=form.question.data)

        db.session.add(new_question)
        db.session.commit()

        return redirect(url_for('faq.faq'))
    return render_template('faq_question.html', form=form)


@faq_blueprint.route('/<int:id>/answer', methods=('GET', 'POST'))
def write_answer(id):
    question = FAQ.query.filter_by(id=id).first()

    form = FAQFormAnswer()

    if form.validate_on_submit():
        FAQ.query.filter_by(id=id).update({"question": form.question.data})
        FAQ.query.filter_by(id=id).update({"answer": form.answer.data})

        db.session.commit()

        return faq()

    # if form isn't valid, create a copy to avoid database locking error
    copy_question = copy.deepcopy(question)

    form.original_question = copy_question.question

    return render_template('faq_answer.html', form=form)
