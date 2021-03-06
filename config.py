import os


class DevConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('PLANET_EFFECT_DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'LongAndRandomSecretKey'

    RECAPTCHA_PUBLIC_KEY = '6LfWFA8eAAAAAC77HTZ2j_1N0eW5q2jN4B-MjIEy'
    RECAPTCHA_PRIVATE_KEY = '6LfWFA8eAAAAAGjnooP2HCUSpOr7I52kRjUpzKop'

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('PLANET_EFFECT_USERNAME')
    MAIL_PASSWORD = os.environ.get('PLANET_EFFECT_PASSWORD')

class TestConfig(DevConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
