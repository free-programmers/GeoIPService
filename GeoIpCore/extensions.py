# flask extensions

import os
from redis import Redis
from flask_mail import Mail
from flask_session import Session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_captcha2 import FlaskCaptcha2
from flask_babel import Babel
from dotenv import load_dotenv
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

load_dotenv()

RedisServer = Redis(
    username=os.environ.get("REDIS_USERNAME", ""),
    password=os.environ.get("REDIS_PASSWORD", ""),
    host=os.environ.get("REDIS_HOST", "localhost"),
    port=os.environ.get("REDIS_PORT", "6379"),
    db=os.environ.get("REDIS_DB", "0"),
)

ServerRequestLimiter = Limiter(
    get_remote_address,
    default_limits=["60 per hour"],
    storage_uri=os.environ.get("LIMITER_REDIS_URI", "redis://localhost:6379"),
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
