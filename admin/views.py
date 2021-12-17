from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import User

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


# view admin page
@admin_blueprint.route('/admin')
@login_required
# MISSING - admin role restriction
def admin():
    return render_template('admin.html', lastname=current_user.lastname)


# view all users
@admin_blueprint.route('/view_users', methods=['POST'])
@login_required
# MISSING - admin role restriction
def view_users():
    return render_template('admin.html', lastname=current_user.lastname,
                           all_users=User.query.all())


# view security logging data (last 15 log records)
@admin_blueprint.route('/logging', methods=['POST'])
@login_required
# MISSING - admin role restriction
def logging():
    # read last 15 log records
    with open("user_logs.log", "r") as f:
        content = f.read().splitlines()[-15:]
        content.reverse()

    return render_template('admin.html', lastname=current_user.lastname, logs=content)
