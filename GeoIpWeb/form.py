from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import Length, DataRequired, InputRequired, Email


class ContactUsForm(FlaskForm):
    """Contact Us Form"""
    Title = StringField(
        validators=[
            DataRequired(),
            InputRequired(),
            Length(min=6, max=255)
        ]
    )

    Email = EmailField(
        validators=[
            Email(),
            DataRequired(),
            InputRequired(),
        ]
    )

    Message = TextAreaField(
        validators=[
            DataRequired(),
            InputRequired(),
            Length(min=6, max=2048)
        ]
    )

    submit = SubmitField(
        render_kw={
            'value': "Send",
            'class': "btn btn-warning px-5"
        }
    )
