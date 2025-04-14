"""
* geoIPservice
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2024 - ali sharifi
* https://github.com/free-programmers/GeoIPService
"""

import os
import pathlib
from pathlib import Path

import redis
from dotenv import load_dotenv

from common_libs.utils import generate_random_string

load_dotenv()


class BaseSetting:
    """Base Setting class"""

    SECRET_KEY: str = os.environ.get("APP_SECRET_KEY", generate_random_string())
    if not os.environ.get("APP_SECRET_KEY", False):
        print(  # TODO: use logger instead of print
            "SECRET_KEY was not found in .env file, fall back "
            "into generate_random_string() function. "
        )
    DEBUG: bool = os.environ.get("APP_DEBUG", "") == "True"
    BASE_DIR: pathlib.Path = Path(__file__).parent.parent.resolve()

    # main API config
    API_NAME: str = os.environ.get("API_NAME", "api-service")
    API_REDOC_URL: str = os.environ.get("API_REDOC_URL", "/redoc")
    API_SWAGGER_URL: str = f'{os.environ.get("API_SWAGGER_URL", "/swagger")}'
    API_ABSOLUTE_VERSION: str = os.environ.get("API_ABSOLUTE_VERSION", "1.0.0")
    API_SHORT_VERSION: str = os.environ.get("API_SHORT_VERSION", "1.0.0")
    API_SUMMERY: str = os.environ.get("API_SUMMERY", "")
    API_DESCRIPTION: str = os.environ.get("API_DESCRIPTION", "")
    API_TERM_URL: str = os.environ.get("API_TERM", "/term")
    API_BASE_URL: str = (
        f"/{os.environ.get('API_BASE_URL', 'api')}/v{API_SHORT_VERSION}/"
    )

    # database config
    DATABASE_NAME: str = os.environ.get("DATABASE_NAME", "")
    DATABASE_PORT: str = os.environ.get("DATABASE_PORT", "")
    DATABASE_HOST: str = os.environ.get("DATABASE_HOST", "")
    DATABASE_USERNAME: str = os.environ.get("DATABASE_USERNAME", "")
    DATABASE_PASSWORD: str = os.environ.get("DATABASE_PASSWORD", "")
    DATABASE_TABLE_PREFIX_NAME: str = os.environ.get("DATABASE_TABLE_PREFIX", "")
    SQLALCHEMY_DATABASE_URI: str = (
        f"postgresql+asyncpg://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    DEBUG_QUERY: bool = os.environ.get("DATABASE_DEBUG_QUERY", "False") == "True"

    def __str__(self):
        return "BaseSetting Class"

    def __repr__(self):
        return self.__str__()


class Setting(BaseSetting):
    """universal config class
    every property on this class will be automatically mapping to app.config
    """

    # redis config
    REDIS_DEFAULT_URI: str = os.environ.get("REDIS_DEFAULT_URI", "localhost")
    REDIS_DEFAULT_INTERFACE = redis.Redis().from_url(REDIS_DEFAULT_URI)

    REDIS_CACHE_URI = os.environ.get("REDIS_CACHE_URI", "localhost")
    REDIS_CACHE_INTERFACE = redis.Redis().from_url(REDIS_CACHE_URI)

    REDIS_API_KEY_URI: str = os.environ.get("REDIS_API_KEY_URI", "localhost")
    REDIS_API_KEY_INTERFACE = redis.Redis.from_url(REDIS_API_KEY_URI)

    #  s3 object storage config
    AWS_BUCKET_NAME: str = os.environ.get("AWS_BUCKET_NAME", "")
    AWS_ACCESS_KEY_ID: str = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_ENDPOINT_URL: str = os.environ.get("AWS_WRITE_ENDPOINT_URL")
    AWS_READ_ENDPOINT_URL: str = os.environ.get("AWS_READ_ENDPOINT_URL")

    # RabbitMQ Config
    RABBITMQ_USERNAME: str = os.environ.get("RABBITMQ_USERNAME")
    RABBITMQ_PASSWORD: str = os.environ.get("RABBITMQ_PASSWORD")
    RABBITMQ_HOST: str = os.environ.get("RABBITMQ_HOST")
    RABBITMQ_PORT: int = (
        5672
        if not os.environ.get("RABBITMQ_PORT").isnumeric()
        else int(os.environ.get("RABBITMQ_PORT"))
    )
    RABBITMQ_VHOST: str = os.environ.get("RABBITMQ_VHOST")

    def __str__(self):
        return "Setting Class"

    def __repr__(self):
        return self.__str__()


class Production(Setting):
    """Production config class

    use this class for Production config class.
    """

    DEBUG: bool = False

    def __str__(self):
        return "Production Config Class"

    def __repr__(self):
        return self.__str__()


class Development(Setting):
    """Development config class

    use this class for Development config class.
    """

    DEBUG: bool = True

    def __str__(self):
        return "Development Config Class"

    def __repr__(self):
        return self.__str__()


def get_config(debug: bool = BaseSetting.DEBUG) -> object:
    """Getting config setting class base on `environment` status.
    :return: object
    :rtype: object
    """
    match debug:
        case True:
            return Development
        case False:
            return Production
        case _:
            return Production