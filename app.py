# IMPORTS
import socket
import logging
from flask import Flask, render_template, request
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from functools import wraps


# LOGGING
class SecurityFilter(logging.Filter):
    def filter(self, record):
        if "USER ACTIVITY" in record.getMessage():
            return True
        elif "SECURITY" in record.getMessage():
            return True
        else:
            return False

fh = logging.FileHandler('user_logs.log', 'w')
fh.setLevel(logging.WARNING)
fh.addFilter(SecurityFilter())
formatter = logging.Formatter('%(asctime)s : %(message)s', '%d/%m/%Y %H:%M:%S')
fh.setFormatter(formatter)

logger = logging.getLogger('')
logger.propagate = False
logger.addHandler(fh)

# CONFIG
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///climate-action.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'LongAndRandomSecretKey'

# initialise database
db = SQLAlchemy(app)

# ROLE ACCESS CONTROL
def required_roles(*roles, source):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.role not in roles:
                logging.warning('SECURITY - Unauthorised access attempt to "%s" [%s, %s, %s]',
                                source, current_user.id, current_user.email, request.remote_addr)
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
    my_host = "127.0.0.1"
    free_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    free_socket.bind((my_host, 0))
    free_socket.listen(5)
    free_port = free_socket.getsockname()[1]
    free_socket.close()

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

    app.run(host=my_host, port=free_port, debug=True)
