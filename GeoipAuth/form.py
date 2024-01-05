from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, HiddenField
from wtforms.validators import DataRequired, InputRequired, Length, EqualTo, Email
from flask_babel import lazy_gettext as _l


class FormFlask(FlaskForm):

    def validate_username(self):
        """
        Validate username contains valid characters

        username should be :
                all #english char
                with #igits
                and with #_

        """
        data = self.Username.data
        from string import ascii_lowercase, digits
        ascii_lowercase = [each for each in ascii_lowercase]
        digits = [each for each in digits]
        valid_char = [*digits, *ascii_lowercase]

        for each in data:
            if each not in valid_char:
                self.Username.errors = [_l("invalid input format"), _l('current format should be like'),
                                        _l("contain alphabet and numbers only")]
                return False

        return True

    def validate(self):
        """Overwrite validate method for checking username"""
        if self.validate_username():
            return super().validate()
        else:
            return False


class LoginForm(FormFlask):
    """Login Users Form"""
    Username = StringField(
        validators=[
            DataRequired(message=_l("data for this field is required!")),
            InputRequired(message=_l("Input for this field is required!")),
            Length(
                min=4,
                max=128,
                message=_l
                ('minimum and maximum length for this field is %(length)s', length="4-128")
            )
        ],
        render_kw={
            "class": "form-control my-2 py-2",
            "placeholder": _l("username")
        }
    )

    Password = PasswordField(
        validators=[
            DataRequired(message=_l("data for this field is required!")),
            InputRequired(message=_l("input for this field is required!")),
            Length(
                min=6,
                max=256,
                message=_l
                ('minimum and maximum length for this field is %(length)s', length="6-256")
            )
        ],
        render_kw={
            "class": "form-control my-2 py-2",
            "placeholder": _l("Password")
        }
    )

    Submit = SubmitField(

        render_kw={
            "value": _l('Login Via Password'),
            "class": "btn bg-danger text-white w-100 py-2 my-3 fs-5 border-0"
        }
    )

