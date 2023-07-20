from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Length, DataRequired, InputRequired


class ContactUSForm(FlaskForm):
    Title = StringField(
        validators=[
            DataRequired(),
            InputRequired(),
            Length(min=6, max=255)
        ]
    )

    Email = StringField(
        validators=[
            DataRequired(),
            InputRequired(),
            Length(min=6, max=255)
        ]
    )

    Message = TextAreaField(
        validators=[
            DataRequired(),
            InputRequired(),
            Length(min=6, max=512)
        ]
    )

    submit = SubmitField()
