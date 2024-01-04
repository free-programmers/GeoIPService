# build in
import os
import datetime
from pathlib import Path

# app
from GeoIpCore.utils import generateRandomString

# libs
import redis
from dotenv import load_dotenv

load_dotenv()

DATABASE_TABLE_PREFIX_NAME = os.environ.get("DATABASE_TABLE_PREFIX_NAME", "")


class Setting:
    """ Flask configuration Class
        base Setting os.environ class for flask app
    """
    BASE_DIR = Path(__file__).parent.parent
    APP_DEBUG_STATUS = os.environ.get("APP_DEBUG", "") == "True"
    SECRET_KEY = os.environ.get("APP_SECRET_KEY", generateRandomString())
    STORAGE_DIR = BASE_DIR.joinpath("Storage")

    # Database Config
    DATABASE_NAME = os.environ.get("DATABASE_NAME", "")
    DATABASE_PORT = os.environ.get("DATABASE_PORT", "")
    DATABASE_HOST = os.environ.get("DATABASE_HOST", "")
    DATABASE_USERNAME = os.environ.get("DATABASE_USERNAME", "")
    DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD", "")
    DATABASE_TABLE_PREFIX_NAME = DATABASE_TABLE_PREFIX_NAME
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Redis Config
    REDIS_URL = os.environ.get("REDIS_URI")
    REDIS_INTERFACE = redis.Redis().from_url(REDIS_URL)
    REDIS_PORT = os.environ.get("REDIS_PORT", "")
    REDIS_HOST = os.environ.get("REDIS_HOST", "")
    REDIS_USERNAME = os.environ.get("REDIS_USERNAME", "")
    REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "")
    REDIS_DB = os.environ.get("REDIS_DB", 0)

    # session cookie setting
    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=24)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_NAME = '_session_cookie_'
    SESSION_REDIS = REDIS_INTERFACE

    # Recaptcha Config <Flask-captcha2>
    RECAPTCHA_PUBLIC_KEY = os.environ.get("RECAPTCHA_PUBLIC_KEY", '')
    RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY", '')
    RECAPTCHA_ENABLED = os.environ.get("RECAPTCHA_ENABLED", False) == "True"
    RECAPTCHA_LOG = os.environ.get("RECAPTCHA_LOG", True) == "True"
    # RECAPTCHA_THEME = ''
    # RECAPTCHA_TYPE = ''
    # RECAPTCHA_SIZE = ''
    # RECAPTCHA_LANGUAGE = ''
    # RECAPTCHA_TABINDEX = ''

    # available languages
    LANGUAGES = {
        'fa': "فارسی/Farsi",
        'en': "English/American English",
        # 'ar': "عربي/Arabic",
        # 'tr': "Turkish/Türkçe",
        # 'ru': "Russian/Россия",
        # 'zh': "Chinese/中国人",
    }

    # Mail config
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT'))
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS') == 'True'
    MAIL_USE_SSL = False
    MAIL_DEBUG = os.environ.get("MAIL_DEBUG") == "True"
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")

    # https: // flask - caching.readthedocs.io / en / latest /  # built-in-cache-backends
    # https: // flask - caching.readthedocs.io / en / latest /  # configuring-flask-caching
    # CACHE_TYPE = "RedisCache"  # NullCache for disable Flask-Caching related os.environs
    CACHE_TYPE = os.environ.get("CACHE_TYPE", 'NullCache')
    CACHE_DEFAULT_TIMEOUT = ((60 * 60) * 12) # seconds
    CACHE_REDIS_HOST = os.environ.get("REDIS_HOST", '')
    CACHE_REDIS_PORT = os.environ.get("REDIS_PORT", '')
    CACHE_REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", '')
    CACHE_REDIS_DB = os.environ.get("CACHE_REDIS_DB", '')
    CACHE_REDIS_URL = (f"redis://{REDIS_HOST}:{REDIS_PORT}/{CACHE_REDIS_DB}")
    # redis: // user: password @ localhost:6379 / 2

    # celery config
    CELERY = dict(
        broker_url=os.environ.get("REDIS_URI_CELERY_BROKER", REDIS_URL),
        result_backend=os.environ.get("REDIS_URI_CELERY_BACKEND", REDIS_URL),
        task_ignore_result=True,
        broker_connection_retry_on_startup=True,
        result_serializer="pickle"
    )

    DEBUG = APP_DEBUG_STATUS
    FLASK_DEBUG = APP_DEBUG_STATUS

    DOMAIN = os.environ.get("SERVER", "")
    SERVER = "127.0.0.1"
