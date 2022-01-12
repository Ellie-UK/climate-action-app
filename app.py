# IMPORTS
import os
import socket
import logging
from flask import Flask, render_template, request
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy

from functools import wraps




# CONFIG
app = Flask(__name__)
app.config.from_object('config.DevConfig')

from mail import mail
mail.init_app(app)
# initialise database
from models import db
db.init_app(app)





# HOME PAGE VIEW
@app.route('/')
def index():
    return render_template('index.html')


from models import User

login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


from users.views import users_blueprint
from admin.views import admin_blueprint

# register blueprints with app
app.register_blueprint(users_blueprint)
app.register_blueprint(admin_blueprint)


if __name__ == '__main__':
    app.run(debug=True)
