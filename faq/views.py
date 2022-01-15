from flask import Blueprint, render_template
from flask_login import login_required
from models import FAQ

faq_blueprint = Blueprint('faq', __name__, template_folder='templates')


@faq_blueprint.route('/faq')
@login_required
def faq():
    questions = FAQ.query.all()
    return render_template('faq.html', questions=questions)
