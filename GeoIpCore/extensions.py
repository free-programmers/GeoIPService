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

load_dotenv()

RedisServer = Redis(
    username=os.environ.get("REDIS_USERNAME", ""),
    password=os.environ.get("REDIS_PASSWORD", ""),
    host=os.environ.get("REDIS_HOST", "localhost"),
    port=os.environ.get("REDIS_PORT", "6379"),
    db=os.environ.get("REDIS_DB", "0"),
)

db = SQLAlchemy()
babel = Babel()
ServerMail = Mail()
ServerSession = Session()
ServerMigrate = Migrate()
ServerCaptcha2 = FlaskCaptcha2()
ServerCache = Cache()
ServerRequestLimiter = Limiter()