# IMPORTS
import os
import socket
from flask import Flask, render_template, request
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from functools import wraps

# CONFIG
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///climate-action.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'LongAndRandomSecretKey'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LeKXrcdAAAAADrogHmxHWzj4kDcX96dj7ZwY7Gl'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LeKXrcdAAAAABItn058xBgvnfJtlsDCle4Unv_m'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
print(os.environ.get('PLANET_EFFECT_USERNAME'))
print(os.environ.get('PLANET_EFFECT_PASSWORD'))
app.config['MAIL_USERNAME'] = os.environ.get('PLANET_EFFECT_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('PLANET_EFFECT_PASSWORD')


mail = Mail(app)
# initialise database
db = SQLAlchemy(app)


# ROLE ACCESS CONTROL
def required_roles(*roles, source):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.role not in roles:
                # redirect user to 403 error page
                return render_template('error_codes/403.html')
            return f(*args, **kwargs)

        return wrapped

    return wrapper


# HOME PAGE VIEW
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    login_manager = LoginManager()
    login_manager.login_view = 'users.login'
    login_manager.init_app(app)

    from models import User


    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    # BLUEPRINTS
    # import blueprints
    from users.views import users_blueprint
    from admin.views import admin_blueprint

    # register blueprints with app
    app.register_blueprint(users_blueprint)
    app.register_blueprint(admin_blueprint)

    app.run(host='0.0.0.0', port=8080, debug=True)
