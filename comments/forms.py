from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired


# form for creating comments
class CommentForm(FlaskForm):
    body = TextAreaField(validators=[DataRequired()])
    submit = SubmitField()
