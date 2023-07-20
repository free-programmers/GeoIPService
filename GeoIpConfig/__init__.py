import os
import datetime
import secrets
from pathlib import Path
from GeoIpCore.extensions import ServerRedis
from dotenv import load_dotenv


BASE_DIR = Path(__file__).parent.parent
load_dotenv()


USERNAME_DB = os.environ.get("X_MYSQL_USERNAME")
PASSWORD_DB = os.environ.get("X_MYSQL_PASSWORD")
HOST_DB = os.environ.get("X_MYSQL_HOST")
PORT_DB = os.environ.get("X_MYSQL_PORT")
NAME_DB = os.environ.get("X_MYSQL_DATABASE_NAME")

BASE_DOMAIN = os.environ.get("X_DOMAIN", "HTTPS://DOMAIN.IR")

class config:
    SECRET_KEY = os.environ.get("X_SECRET_KEY", secrets.token_hex(128))
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USERNAME_DB}:{PASSWORD_DB}@{HOST_DB}:{PORT_DB}/{NAME_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # session configuration
    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=16)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_NAME = '_session_cookie_'
    SESSION_USE_SIGNER = True
    SESSION_REDIS = ServerRedis

    # recaptcha v2
    RECAPTCHA_PUBLIC_KEY = os.environ.get("X_CAPTCHA_PUBLIC")
    RECAPTCHA_PRIVATE_KEY = os.environ.get("X_CAPTCHA_PRIVATE")
    RECAPTCHA_ENABLED = os.environ.get("X_CAPTCHA_ENABLE", True)

    # caching config
    # CACHE_TYPE = "RedisCache"  # NullCache for disable Flask-Caching related configs
    CACHE_TYPE = os.environ.get("X_CACHE_TYPE")
    CACHE_DEFAULT_TIMEOUT = ((60*60)*12)
    CACHE_REDIS_HOST = os.environ.get("X_REDIS_HOST")
    CACHE_REDIS_PORT = os.environ.get("X_REDIS_PORT")
    CACHE_REDIS_PASSWORD = os.environ.get("X_REDIS_PASSWORD")
    CACHE_REDIS_DB = os.environ.get("X_REDIS_DB")
    CACHE_REDIS_URL = os.environ.get("X_REDIS_URL")


    DEBUG = True if os.environ.get("X_DEBUG") == 'True' else False
    FLASK_DEBUG = True if os.environ.get("X_DEBUG") == 'True' else False


