from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Email, Length, EqualTo, ValidationError, DataRequired
from models import User


class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    pin = StringField(validators=[DataRequired(), Length(min=6, max=6, message='Pin must be 6 digits long')])
    recaptcha = RecaptchaField()

    submit = SubmitField()


class RegisterForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    firstname = StringField(validators=[DataRequired()])
    lastname = StringField(validators=[DataRequired()])
    phone = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired(), Length(min=6, max=12, message='Password must be between 6 and 12 characters in length.')])
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo('password', message='Both password fields must be equal!')])
    pin_key = StringField(validators=[DataRequired(), Length(min=32, max=32, message='pin key must be 32 characters in length.')])
    submit = SubmitField()

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(validators=[DataRequired()])
    new_password = PasswordField(validators=[DataRequired(), Length(min=6, max=12, message='Password must be between 6 and 12 characters in length.')])
    confirm_new_password = PasswordField(validators=[DataRequired(), EqualTo('new_password', message='Both password fields must be equal!')])
    submit = SubmitField()

class RequestResetForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    submit = SubmitField()

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField(validators=[DataRequired(), Length(min=6, max=12, message='Password must be between 6 and 12 characters in length.')])
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo('password', message='Both password fields must be equal!')])
    submit = SubmitField()