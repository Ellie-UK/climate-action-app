from flask import Blueprint, render_template

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


# view admin page
@admin_blueprint.route('/admin')
# add access restrictions
def admin():
    return render_template('admin.html', lastname="PLACEHOLDER FOR LASTNAME")
