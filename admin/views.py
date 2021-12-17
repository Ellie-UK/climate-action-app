from flask import Blueprint, render_template
from models import User

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


# view admin page
@admin_blueprint.route('/admin')
# MISSING - add access restrictions
def admin():
    return render_template('admin.html', lastname="PLACEHOLDER FOR LASTNAME")


# view all users
@admin_blueprint.route('/view_users', methods=['POST'])
# MISSING - add access restrictions
def view_users():
    return render_template('admin.html', lastname="PLACEHOLDER FOR LASTNAME",
                           all_users=User.query.all())
