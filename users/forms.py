from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required, Email, Length, EqualTo


class LoginForm(FlaskForm):
    email = StringField(validators=[Required(), Email()]) #Need to implement error code in to login.html, for it to show error message when triggered
    password = PasswordField(validators=[Required()]) #Need to implement error code in to login.html, for it to show error message when triggered
    pin = StringField(validators=[Required(), Length(min=6, max=6, message='Pin must be 6 digits long')]) #Need to implement error code in to login.html, for it to show error message when triggered
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