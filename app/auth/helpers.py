import bcrypt 
from app import login_manager
from flask_login import UserMixin
from flask import flash, redirect, session, url_for
from .models import User

@login_manager.user_loader
def load_user(user_id):
    # Check if the user exists in the session, if yes, return it
    if 'user' in session:
        user_data = session['user']
        return User.query.get(user_data['id'])
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('Error: You must be logged in to access this page.', 'danger')
    return redirect(url_for('auth_views.login'))
