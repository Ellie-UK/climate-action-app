# IMPORTS
from datetime import datetime

import flask
from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_user, logout_user, login_required
from flask_mail import Message
from sqlalchemy import text, select

from mail import mail
from models import User, db
from users.forms import RegisterForm, LoginForm, ChangePasswordForm, ResetPasswordForm, RequestResetForm
from werkzeug.security import check_password_hash, generate_password_hash
import pyotp

users_blueprint = Blueprint('users', __name__, template_folder='templates')


def check_subscription(user_id):
    subUser = User.query.filter_by(id=user_id).first()
    return subUser.subscribed == 1

def get_subscribed():
    users = User.query.filter_by(subscribed=1)
    for user in users:
        print(user.email)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply.planeteffect@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

# view user login
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # if session attribute logins does not exist create attribute logins
    if not session.get('logins'):
        isDisabled = False
        session['logins'] = 0
    # if login attempts is 3 or more create an error message
    elif session.get('logins') >= 3:
        isDisabled = True
        flash('Number of incorrect logins exceeded')
    # if login attempt is 1 or 2
    else:
        isDisabled = False

    form = LoginForm()

    if form.validate_on_submit():

        # increase login attempts by 1
        session['logins'] += 1

        user = User.query.filter_by(email=form.email.data).first()

        if not user or not check_password_hash(user.password, form.password.data):

            # if no match it would flash appropriate error message based on login attempts
            if session['logins'] == 3:
                flash('Number of incorrect logins exceeded')
                isDisabled = True
            elif session['logins'] == 2:
                flash('Please check your login details and try again. 1 login attempt remaining')
                isDisabled = False
            else:
                flash('Please check your login details and try again. 2 login attempts remaining')
                isDisabled = False
            return render_template('login.html', form=form, isDisabled=isDisabled)

        isDisabled = False
        if pyotp.TOTP(user.pin_key).verify(form.pin.data):
            login_user(user)

            # if user is verified reset login attempts to 0
            session['logins'] = 0

            user.last_logged_in = user.current_logged_in
            user.current_logged_in = datetime.now()
            db.session.add(user)
            db.session.commit()
        else:
            flash("You have supplied an invalid 2FA token!")

        return account()
    return render_template('login.html', form=form, isDisabled=isDisabled)


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
    return render_template('account.html',
                           acc_no=current_user.id,
                           email=current_user.email,
                           firstname=current_user.firstname,
                           lastname=current_user.lastname,
                           phone=current_user.phone,
                           registered=current_user.registered_on.strftime("%x"),
                           role=current_user.role,
                           user_subscribed=check_subscription(current_user.id))


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




@users_blueprint.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users_blueprint.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = generate_password_hash(form.password.data)
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


# view logout
@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirectpage("Logged out successfully", 3, url_for('index'))


@users_blueprint.route('/deleteaccount', methods=['POST', 'GET'])
@login_required
def deleteaccount():
    if current_user.role == 'admin':
        return redirectpage("ERROR: Admin accounts cannot be deleted", 3, url_for('users.account'))
    id = current_user.id
    user_to_delete = User.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirectpage("Account deleted successfully", 3, url_for('index'))
    except:
        return redirectpage("Something went wrong, please try again later", 3, url_for('index'))


@users_blueprint.route('/climate_page')
def climate_data():
    return render_template('climate_data.html')


@users_blueprint.route('/modify_subscription')
def modify_subscription():
    current_user.subscribed = 1 - current_user.subscribed

    db.session.commit()
    if check_subscription(current_user.id):
        return redirectpage("Subscribed successfully!", 3, url_for('users.account'))
    else:
        return redirectpage("Unsubscribed successfully!", 3, url_for('users.account'))

@users_blueprint.route('/redirectpage', methods=['GET'])
def redirectpage(message, wait, pointer):
    return render_template('redirectpage.html', message=message, wait=wait, pointer=pointer)
