# from crypt import methods
from flask import render_template, url_for, redirect, request, Blueprint
from flask_login import current_user
from app import app, db
from flask_login import login_required

main_views=Blueprint('main_views', __name__)

# Making a simple log in app, that returns your data
@main_views.route('/', methods=["POST", "GET"])
def landing_page():
    if request.method == 'POST':
        if request.form['submit'] == 'Login':
            return redirect(url_for('login'))

        elif request.form['submit'] == 'Register':
            return redirect(url_for('register'))

        elif request.form['submit'] == 'Delete':
            return redirect(url_for('delete'))

        else:
            return redirect(url_for('logout'))
    return render_template('home.html')


@main_views.route('/home')
@login_required
def home():
    return render_template('home.html', current_user=current_user)


@main_views.route('/about')
def about():
    return render_template('about.html')


##############################################################################################################

@app.errorhandler(404)
def not_found_error(error):
    return "Whoops! <br> <a href='/'>Return Home!</a>"


@app.errorhandler(500)
def internal_error():
    db.sesssion.rollback()
    return "Whoops! <br> <a href='/'>Return Home!</a>"
