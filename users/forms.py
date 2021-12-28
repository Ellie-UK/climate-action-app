from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required, Email, Length, EqualTo


class LoginForm(FlaskForm):
    email = StringField(validators=[Required(), Email()])
    password = PasswordField(validators=[Required()])
    pin = StringField(validators=[Required(), Length(min=6, max=6, message='Pin must be 6 digits long')])
    recaptcha = RecaptchaField()

    submit = SubmitField()


class RegisterForm(FlaskForm):
    email = StringField(validators=[Required(), Email()])
    firstname = StringField(validators=[Required()])
    lastname = StringField(validators=[Required()])
    phone = StringField(validators=[Required()])
    password = PasswordField(validators=[Required(), Length(min=6, max=12, message='Password must be between 6 and 12 characters in length.')])
    confirm_password = PasswordField(validators=[Required(), EqualTo('password', message='Both password fields must be equal!')])
    pin_key = StringField(validators=[Required(), Length(min=32, max=32, message='pin key must be 32 characters in length.')])
    submit = SubmitField()

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(validators=[Required()])
    new_password = PasswordField(validators=[Required(), Length(min=6, max=12, message='Password must be between 6 and 12 characters in length.')])
    confirm_new_password = PasswordField(validators=[Required(), EqualTo('new_password', message='Both password fields must be equal!')])
    submit = SubmitField()
