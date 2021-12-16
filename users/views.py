# IMPORTS
from datetime import datetime

import flask
from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_user, logout_user, login_required

from app import db
from models import User
from users.forms import RegisterForm, LoginForm, ChangePasswordForm
from werkzeug.security import check_password_hash, generate_password_hash
import pyotp

users_blueprint = Blueprint('users', __name__, template_folder='templates')


# view user login
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if not user or not check_password_hash(user.password, form.password.data):
            flash('Please check your login details and try again')
            return render_template('login.html', form=form)

        login_user(user)

        user.last_logged_in = user.current_logged_in
        user.current_logged_in = datetime.now()
        db.session.add(user)
        db.session.commit()

        return account()
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


@users_blueprint.route('/account')
@login_required
def account():
    print("wow!")
    return render_template('account.html',
                           acc_no=current_user.id,
                           email=current_user.email,
                           firstname=current_user.firstname,
                           lastname=current_user.lastname,
                           phone=current_user.phone)

@users_blueprint.route('/changepassword', methods=['GET', 'POST'])
@login_required
def changepassword():
    form = ChangePasswordForm()
    # if request method is POST or form is valid
    if form.validate_on_submit():
        if not check_password_hash(current_user.password, form.current_password.data):
            flash('Current password is incorrect')
            return render_template('changepassword.html', form=form)
        current_user.password = generate_password_hash(form.new_password.data)
        db.session.commit()
        return redirectpage("Your password was changed successfully", 3, url_for('users.account'))
    return render_template('changepassword.html', form=form)

# view logout
@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirectpage("Logged out successfully", 3, url_for('index'))

@users_blueprint.route('/redirectpage', methods=['GET'])
def redirectpage(message, wait, pointer):
    return render_template('redirectpage.html', message=message, wait=wait, pointer=pointer)