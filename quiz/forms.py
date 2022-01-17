from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired


class QuizForm(FlaskForm):
    question = StringField(validators=[DataRequired()])
    option1 = TextAreaField(validators=[DataRequired()])
    option2 = TextAreaField(validators=[DataRequired()])
    option3 = TextAreaField()
    option4 = TextAreaField()
    answer = IntegerField(validators=[DataRequired()])
    submit = SubmitField()