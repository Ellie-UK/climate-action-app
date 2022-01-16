from faq.forms import FAQFormQuestion
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
