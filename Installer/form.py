from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, InputRequired


class DatabaseINIT(FlaskForm):
    """Database init information in installation <form>"""
    DatabaseName = StringField(
        validators=[
            DataRequired(),
            InputRequired()
        ]
    )

    DatabaseUsername = StringField(
        validators=[
            DataRequired(),
            InputRequired()
        ]
    )

    DatabaseUserPassword = PasswordField(
        validators=[
            DataRequired(),
            InputRequired()
        ]
    )

    DatabaseHost = StringField(
        validators=[
            DataRequired(),
            InputRequired()
        ]
    )
    DatabaseTablePrefix = StringField(
        validators=[
            DataRequired(),
            InputRequired()
        ]
    )

    DataBasePort = IntegerField(
        validators=[
            DataRequired(),
            InputRequired()
        ]
    )


    submit = SubmitField()