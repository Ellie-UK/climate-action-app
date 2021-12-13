from flask import Blueprint, render_template, flash, redirect, url_for
from users.forms import LoginForm, RegisterForm
from models import User
from app import db

users_blueprint = Blueprint('users', __name__, template_folder='templates')


# view user login
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        return login()
    return render_template('login.html', form=form)

@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    # if request method is POST or form is valid
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # if this returns a user, then the email already exists in database

        # if email already exists redirect user back to signup page with error message so user can try again
        if user:
            flash('Email address already exists')
            return render_template('register.html', form=form)

        # create a new user with the form data
        new_user = User(email=form.email.data,
                        firstname=form.firstname.data,
                        lastname=form.lastname.data,
                        phone=form.phone.data,
                        password=form.password.data,
                        pin_key=form.pin_key.data,
                        role='user')

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # sends user to login page
        return redirect(url_for('users.login'))

    return render_template('register.html', form=form)

