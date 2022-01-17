from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required


class FAQFormQuestion(FlaskForm):
    question = StringField(validators=[Required()])
    submit = SubmitField()


class FAQFormAnswer(FlaskForm):
    question = StringField(validators=[Required()])
    answer = TextAreaField(validators=[Required()])
    original_question = ""
    submit = SubmitField()
