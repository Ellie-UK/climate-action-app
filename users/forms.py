from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required, Email, Length


class LoginForm(FlaskForm):
    email = StringField(validators=[Required(), Email()]) #Need to implement error code in to login.html, for it to show error message when triggered
    password = PasswordField(validators=[Required()]) #Need to implement error code in to login.html, for it to show error message when triggered
    pin = StringField(validators=[Required(), Length(min=6, max=6, message='Pin must be 6 digits long')]) #Need to implement error code in to login.html, for it to show error message when triggered
    submit = SubmitField()


