from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


# Form for creating questions
class FAQFormQuestion(FlaskForm):
    question = StringField(validators=[DataRequired()])
    submit = SubmitField()


# Form for answering questions
class FAQFormAnswer(FlaskForm):
    question = StringField(validators=[DataRequired()])
    answer = TextAreaField(validators=[DataRequired()])
    original_question = ""
    submit = SubmitField()
