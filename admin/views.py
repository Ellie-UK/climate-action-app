from flask import Blueprint, render_template
from models import User

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


# view admin page
@admin_blueprint.route('/admin')
# MISSING - add access restrictions
def admin():
    return render_template('admin.html', lastname="PLACEHOLDER FOR LASTNAME")


# view all registered users
@admin_blueprint.route('/view_users', methods=['POST'])
# MISSING - add access restrictions
def view_users():
    return render_template('admin.html', lastname="PLACEHOLDER FOR LASTNAME",
                           all_users=User.query.filter_by(role='user').all())


# view logging (last 15 log records)
@admin_blueprint.route('/logging', methods=['POST'])
# MISSING - add access restrictions
def logging():
    # MISSING - create 'user_logs.log' that contains logging data
    with open("user_logs.log", "r") as f:
        content = f.read().splitlines()[-15:]
        content.reverse()

    return render_template('admin.html', lastname="PLACEHOLDER FOR LASTNAME", logs=content)
