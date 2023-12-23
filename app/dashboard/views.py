from flask import render_template, url_for, flash, redirect, Blueprint
from flask_login import current_user
from app.auth.models import User
from flask_login import login_required

dashboard_views=Blueprint('dashboard_views', __name__)

@dashboard_views.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_admin():
        flash('Error: You do not have permission to access this page.', 'danger')
        return redirect(url_for('home'))
    total_users = User.query.count()
    # Count the number of logged-in users
    logged_in_users = len(
        [user for user in User.query.all() if user.is_authenticated])
    return render_template('dashboard.html', total_users=total_users, logged_in_users=logged_in_users)
