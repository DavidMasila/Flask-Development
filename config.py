#creating configuration classes
import secrets

class Config:
    DEBUG = False
    TESTING = False
    secret_key = secrets.token_hex(16)
    SECRET_KEY = secret_key

    DB_NAME = "production-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "password"

    UPLOADS = "/home/username/app/app/static/images/uploads"
    SESSION_COOKIE_SECURE =True

class Production(Config):
    pass

class Development(Config):
    DEBUG = True

    DB_NAME = "development-db"
    UPLOADS = "/home/username/projects/flask_test/app/app/static/images/uploads"
    SESSION_COOKIE_SECURE = False


class Testing(Config):
    TESTING = True

    DB_NAME = "development-db"
    SESSION_COOKIE_SECURE = False