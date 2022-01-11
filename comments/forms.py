from wtforms import Form, StringField, SubmitField
from wtforms.validators import DataRequired


class CommentForm(Form):
    body = StringField('', validators=[DataRequired()])
    submit = SubmitField('Submit')