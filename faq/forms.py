from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class FAQFormQuestion(FlaskForm):
    question = StringField(validators=[DataRequired()])
    submit = SubmitField()


class FAQFormAnswer(FlaskForm):
    question = StringField(validators=[DataRequired()])
    answer = TextAreaField(validators=[DataRequired()])
    original_question = ""
    submit = SubmitField()
