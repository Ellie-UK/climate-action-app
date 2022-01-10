from flask import Blueprint, render_template
from flask_login import login_required

forum_blueprint = Blueprint('forum', __name__, template_folder='templates')


@forum_blueprint.route('/forum')
@login_required
def forum():
    return render_template('/forum.html')