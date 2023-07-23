import configparser

config = configparser.ConfigParser()

config["database"] = {
    'X_MYSQL_USERNAME': 'root',
    'X_MYSQL_PASSWORD': '',
    'X_MYSQL_HOST': 'localhost',
    'X_MYSQL_PORT': '3306',
    'X_MYSQL_DATABASE_NAME': 'geoip',
}
config["captcha"] = {
    'X_CAPTCHA_PUBLIC': ' ',
    'X_CAPTCHA_PRIVATE': ' ',
    'X_CAPTCHA_ENABLE': False,
}

config["app"] ={
    'X_SECRET_KEY': 'hi :)',
    'X_DEBUG': True,
    'X_DOMAIN': 'https://www.geoip.ir',
}

config["cache"] = {
    'X_CACHE_TYPE': 'RedisCache',
}

config["redis"] = {
    'X_REDIS_HOST': 'localhost',
    'X_REDIS_PORT': '6379',
    'X_REDIS_PASSWORD': '',
    'X_REDIS_DB': '0',
    'X_REDIS_URL': 'redis://:@localhost:6379/0'
}

with open("config.ini", mode="w", encoding="utf-8") as f:
    config.write(f)
