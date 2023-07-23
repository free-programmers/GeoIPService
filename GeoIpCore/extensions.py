from redis import Redis
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_captcha2 import FlaskCaptcha2
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from configparser import ConfigParser


config = ConfigParser()
config.read('config.ini')

ServerRedis = Redis().from_url(config.get(section='redis', option="X_REDIS_URL", fallback=''))
SessionServer = Session()
db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
limiter = Limiter(
  get_remote_address,
  storage_uri=config.get(section='redis', option="X_REDIS_URL", fallback=''),
  storage_options={"socket_connect_timeout": 30},
  strategy="fixed-window", # or "moving-window"
)
cache = Cache()
captchaVersion2 = FlaskCaptcha2()
