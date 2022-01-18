from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired


# flask form for creating a quiz question
class QuizForm(FlaskForm):
    question = StringField(validators=[DataRequired()])
    option1 = TextAreaField(validators=[DataRequired()])
    option2 = TextAreaField(validators=[DataRequired()])
    option3 = TextAreaField(validators=[DataRequired()])
    option4 = TextAreaField(validators=[DataRequired()])
    answer = IntegerField(validators=[DataRequired()])
    submit = SubmitField()