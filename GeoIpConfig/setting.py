import datetime
import secrets
from pathlib import Path
from GeoIpCore.extensions import ServerRedis
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
BASE_DIR = Path(__file__).parent.parent

USERNAME_DB = config.get(section="database", option="X_MYSQL_USERNAME", fallback="")
PASSWORD_DB = config.get(section="database", option="X_MYSQL_PASSWORD", fallback="")
HOST_DB = config.get(section="database", option="X_MYSQL_HOST", fallback="")
PORT_DB = config.get(section="database", option="X_MYSQL_PORT", fallback="")
NAME_DB = config.get(section="database", option="X_MYSQL_DATABASE_NAME", fallback="")

BASE_DOMAIN = config.get(section="app", option="X_DOMAIN", fallback="HTTPS://DOMAIN.IR")


class Config:
    SECRET_KEY = config.get(section="app", option="X_SECRET_KEY", fallback=secrets.token_hex(128))
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
    RECAPTCHA_PUBLIC_KEY = config.get(section='captcha', option="X_CAPTCHA_PUBLIC", fallback='')
    RECAPTCHA_PRIVATE_KEY = config.get(section='captcha', option="X_CAPTCHA_PRIVATE", fallback='')
    RECAPTCHA_ENABLED = config.get(section='captcha', option="X_CAPTCHA_ENABLE", fallback=False)

    # caching config
    # CACHE_TYPE = "RedisCache"  # NullCache for disable Flask-Caching related configs
    CACHE_TYPE = config.get(section='cache', option="X_CACHE_TYPE", fallback='NullCache')
    CACHE_DEFAULT_TIMEOUT = ((60 * 60) * 12)
    CACHE_REDIS_HOST = config.get(section='redis', option="X_REDIS_HOST", fallback='')
    CACHE_REDIS_PORT = config.get(section='redis', option="X_REDIS_PORT", fallback='')
    CACHE_REDIS_PASSWORD = config.get(section='redis', option="X_REDIS_PASSWORD", fallback='')
    CACHE_REDIS_DB = config.get(section='redis', option="X_REDIS_DB", fallback='')
    CACHE_REDIS_URL = config.get(section='redis', option="X_REDIS_URL", fallback='')

    DEBUG = True if config.get(section='app', option="X_DEBUG", fallback=False) else False
    FLASK_DEBUG = True if config.get(section='app', option="X_DEBUG", fallback=False) else False


class Development(Config):
    ...


class Production(Config):
    ...


