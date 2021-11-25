from flask import Blueprint, render_template

users_blueprint = Blueprint('users', __name__, template_folder='templates')


# view user login
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')