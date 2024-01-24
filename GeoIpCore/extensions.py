# flask extensions

import os
from flask_mail import Mail
from flask_session import Session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_captcha2 import FlaskCaptcha2
from flask_babel import Babel
from dotenv import load_dotenv
from flask_caching import Cache
from flask_limiter import Limiter

from .utils import user_real_ip
load_dotenv()


ServerRequestLimiter = Limiter(
    user_real_ip,
    storage_uri=os.environ.get("LIMITER_REDIS_URI", ""),
    storage_options={"socket_connect_timeout": 30},
    strategy="fixed-window",  # or "moving-window"
)

db = SQLAlchemy()
babel = Babel()
ServerMail = Mail()
ServerSession = Session()
ServerMigrate = Migrate()
ServerCaptcha2 = FlaskCaptcha2()
ServerCache = Cache()
