# IMPORTS
import os
import socket
import logging
import models
from flask import Flask, render_template, request
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path

from functools import wraps

# CONFIG
app = Flask(__name__)
app.config.from_object('config.DevConfig')

# initialise mail
from mail import mail

mail.init_app(app)
# initialise database
from models import db

db.init_app(app)


# HOME PAGE VIEW
@app.route('/')
def index():
    return render_template('index.html', current_user=current_user)

# ERROR PAGE VIEWS
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error_codes/404.html', current_user=current_user), 404


# initialise login manager
from models import User

login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


# import blueprints
from users.views import users_blueprint
from admin.views import admin_blueprint
from forum.views import forum_blueprint
from faq.views import faq_blueprint
from quiz.views import quiz_blueprint

# register blueprints with app
app.register_blueprint(users_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(forum_blueprint)
app.register_blueprint(quiz_blueprint)
app.register_blueprint(faq_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
