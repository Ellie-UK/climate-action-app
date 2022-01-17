from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

class SendNewsletter(FlaskForm):
    subject = StringField(validators=[DataRequired()])
    body = StringField(validators=[DataRequired()])

    submit = SubmitField()