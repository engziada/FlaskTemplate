# from crypt import methods
from flask import render_template, session, url_for, flash, redirect, Blueprint
from flask_login import current_user
from app import db
from .forms import AddUserForm, LoginForm, EditUserForm
from .models import User
from flask_login import login_user, logout_user, login_required


auth_views=Blueprint("auth_views", __name__, template_folder='templates')

# Login route
@auth_views.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_views.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            # After successful login, store user data in the session
            session['user'] = {
                'id': user.id,
                'username': user.username,
                'rank': user.rank
            }
            return redirect(url_for('main_views.home'))
        else:
            flash('Error: Invalid username or password.', 'danger')
            return redirect(url_for('auth_views.login'))
    return render_template('login.html', form=form)



@auth_views.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user', None)
    return redirect(url_for('auth_views.login'))

##############################################################################################################
'''
Admin routes
'''

# Add user route
@auth_views.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if not current_user.is_admin():
        flash('Error: You do not have permission to access this page.', 'danger')
        return redirect(url_for('main_views.home'))
    form = AddUserForm()
    if form.validate_on_submit():
        username = form.username.data
        email= form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        rank = form.rank.data  # Get the value of 'rank' from the form
        
        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()
        
        if existing_user:
            flash('Error: Username already exists.', 'danger')
            return redirect(url_for('auth_views.add_user'))
        elif existing_email:
            flash('Error: Email already exists.', 'danger')
            return redirect(url_for('auth_views.add_user'))
        else:
            new_user = User(username=username, rank=rank, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Done: New user added successfully!', 'success')
            return redirect(url_for('auth_views.users'))
    return render_template('add_user.html', form=form)


# Users route
@auth_views.route('/users')
@login_required
def users():
    if not current_user.is_admin():
        flash('Error: You do not have permission to access this page.', 'danger')
        return redirect(url_for('main_views.home'))
    users = User.query.all()
    return render_template('users.html', users=users)


# Edit user route
@auth_views.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if not current_user.is_admin():
        flash('Error: You do not have permission to access this page.', 'danger')
        return redirect(url_for('main_views.home'))
    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.rank = form.rank.data  # Get the value of 'rank' from the form
        db.session.commit()
        flash('Done: User details updated successfully!', 'success')
        return redirect(url_for('auth_views.users'))
    return render_template('edit_user.html', form=form)


# Delete user route
@auth_views.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin():
        flash('Error: You do not have permission to access this page.', 'danger')
        return redirect(url_for('main_views.home'))
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Done: User deleted successfully!', 'success')
    return redirect(url_for('auth_views.users'))

