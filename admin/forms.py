from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required, Email, Length, EqualTo, ValidationError

class SendNewsletter(FlaskForm):
    subject = StringField(validators=[Required()])
    body = StringField(validators=[Required()])

    submit = SubmitField()