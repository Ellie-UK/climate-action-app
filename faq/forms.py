from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required


class FAQFormQuestion(FlaskForm):
    question = StringField(validators=[Required()])
    submit = SubmitField()
