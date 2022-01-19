from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SendNewsletter(FlaskForm):
    subject = StringField(validators=[DataRequired()])
    body = StringField(validators=[DataRequired()])

    submit = SubmitField()