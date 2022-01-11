import os

class DevConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///climate-action.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'LongAndRandomSecretKey'
    RECAPTCHA_PUBLIC_KEY = '6LeKXrcdAAAAADrogHmxHWzj4kDcX96dj7ZwY7Gl'
    RECAPTCHA_PRIVATE_KEY = '6LeKXrcdAAAAABItn058xBgvnfJtlsDCle4Unv_m'

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('PLANET_EFFECT_USERNAME')
    MAIL_PASSWORD = os.environ.get('PLANET_EFFECT_PASSWORD')


