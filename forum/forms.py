from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


# flask form for creating a forum post
class ForumForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    body = TextAreaField(validators=[DataRequired()])
    submit = SubmitField()