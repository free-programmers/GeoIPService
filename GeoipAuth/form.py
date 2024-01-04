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
                self.Username.errors = [_l("فرمت ورودی اطلاعات نادرست است"), _l('فرمت درست اطلاعات شامل موارد زیر است'),
                                        _l("شامل اعداد و حروف انگلیسی")]
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
            DataRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
            InputRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
            Length(
                min=4,
                max=128,
                message=_l
                ('حداقل و حداکثر طول فیلد وارد شده باید %(length)s باشد', length="4-128")
            )
        ],
        render_kw={
            "class": "form-control my-2 py-2",
            "placeholder": _l("نام کاربری")
        }
    )

    Password = PasswordField(
        validators=[
            DataRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
            InputRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
            Length(
                min=6,
                max=256,
                message=_l
                ('حداقل و حداکثر طول فیلد وارد شده باید %(length)s باشد', length="6-256")
            )
        ],
        render_kw={
            "class": "form-control my-2 py-2",
            "placeholder": _l("گذرواژه")
        }
    )

    Submit = SubmitField(

        render_kw={
            "value": _l('ورود با گذرواژه'),
            "class": "btn bg-orange text-white w-100 py-2 my-3 fs-5 border-0"
        }
    )


class RegisterForm(FormFlask):
    """Register Users Form"""
    Username = StringField(
        validators=[
            DataRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
            InputRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
            Length(
                min=4,
                max=128,
                message=_l
                ('حداقل و حداکثر طول فیلد وارد شده باید %(length)s باشد', length="4-128")
            )
        ],
        render_kw={
            "class": "form-control my-2 py-2",
            "placeholder": _l("نام کاربری")
        }
    )

    Password = PasswordField(
        validators=[
            DataRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
            InputRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
            Length(
                min=6,
                max=256,
                message=_l
                ('حداقل و حداکثر طول فیلد وارد شده باید %(length)s باشد', length="6-256")
            )
        ],
        render_kw={
            "class": "form-control my-2 py-2",
            "placeholder": _l("گذرواژه")
        }
    )

    PasswordConfirm = PasswordField(
        validators=[
            EqualTo("Password", message=_l("گذرواژه ها یکسان نمی باشد!")),
            DataRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
            InputRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
            Length(
                min=6,
                max=256,
                message=_l
                ('حداقل و حداکثر طول فیلد وارد شده باید %(length)s باشد', length="6-256")
            )
        ],
        render_kw={
            "class": "form-control my-2 py-2",
            "placeholder": _l("تکرار گذرواژه")
        }
    )

    EmailAddress = EmailField(
        validators=[
            Email(message=_l(" آدرس ایمیل وارد شده نامعتبر می باشد ")),
            DataRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
            InputRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
            Length(
                min=4,
                max=256,
                message=_l
                ('حداقل و حداکثر طول فیلد وارد شده باید %(length)s باشد', length="11-256")
            )
        ],
        render_kw={
            "class": "form-control my-2 py-2 text-start",
            "placeholder": _l("آدرس ایمیل")
        }
    )

    Submit = SubmitField(
        render_kw={
            "value": _l('ساخت حساب کاربری'),
            "class": "btn bg-orange text-white w-100 py-2 my-3 fs-5 border-0"
        })


class ForgetPasswordForm(FlaskForm):
    EmailAddress = EmailField(
        validators=[
            Email(message=_l(" آدرس ایمیل وارد شده نامعتبر می باشد ")),
            DataRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
            InputRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
            Length(
                min=4,
                max=256,
                message=_l
                ('حداقل و حداکثر طول فیلد وارد شده باید %(length)s باشد', length="11-256")
            )
        ],
        render_kw={
            "class": "form-control my-2 py-2 text-start",
            "placeholder": _l("آدرس ایمیل")
        }
    )

    Submit = SubmitField(
        render_kw={
            "value": _l('بازنشانی گذرواژه'),
            "class": "btn bg-orange text-white w-100 py-2 my-3 fs-5 border-0"
        })


class SetNewPasswordForm(FlaskForm):
    Password = PasswordField(
        validators=[
            DataRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
            InputRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
            Length(
                min=6,
                max=256,
                message=_l
                ('حداقل و حداکثر طول فیلد وارد شده باید %(length)s باشد', length="6-256")
            )
        ],
        render_kw={
            "class": "form-control my-2 py-2",
            "placeholder": _l("گذرواژه")
        }
    )

    PasswordConfirm = PasswordField(
        validators=[
            EqualTo("Password", message=_l("گذرواژه ها یکسان نمی باشد!")),
            DataRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
            InputRequired(message=_l("وارد کردن داده در این فیلد الزامی است")),
            Length(
                min=6,
                max=256,
                message=_l
                ('حداقل و حداکثر طول فیلد وارد شده باید %(length)s باشد', length="6-256")
            )
        ],
        render_kw={
            "class": "form-control my-2 py-2",
            "placeholder": _l("تکرار گذرواژه")
        }
    )

    Token = HiddenField()
    Submit = SubmitField(
        render_kw={
            "value": _l('بازنشانی گذرواژه'),
            "class": "btn bg-orange text-white w-100 py-2 my-3 fs-5 border-0"
        })