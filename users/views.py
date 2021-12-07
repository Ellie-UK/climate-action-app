from flask import Blueprint, render_template

from users.forms import LoginForm

users_blueprint = Blueprint('users', __name__, template_folder='templates')


# view user login
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        return login()
    return render_template('login.html', form=form)