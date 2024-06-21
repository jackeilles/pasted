from werkzeug.datastructures import FileStorage
from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, logout_user, login_user, login_required
import os
import datetime
from app import app, db
from app.models import User
from app.forms import LoginForm, RegistrationForm
import magic
import sqlalchemy as sa


@app.route('/', methods=["GET", "POST"])
def index():
    # Initial data for the index page
    hex_rand: str = os.urandom(15).hex()
    timestamp: int = int(datetime.datetime.now().timestamp())

    if request.method == "GET":
        return render_template('index.html', title='Anonymous, Private, Secure, and Temporary.', hex_rand=hex_rand, timestamp=timestamp, user="")
    elif request.method == "POST":
        # We're gonna grab the form data from the request first.
        fdata = request.form

        # If this try except fails then the data is inside of the form rather than a file.
        try:
            data: FileStorage = request.files['file']
            data.seek(0)
            mime: str = magic.from_buffer(data.read(1024), mime=True) # This will be needed when loading the file in browser.
        except KeyError:
            data: str = fdata['file'] # Just toss the stuff from the form into data instead
            mime: str = "text/plain"

        # We will check whether the MIME type of the file is disallowed.

@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    login_form = LoginForm()
    register_form = RegistrationForm()

    if login_form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == login_form.username.data))
        if user is None or not user.pass_check(login_form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=login_form.remember.data)
        return redirect(url_for('index'))
    
    if register_form.validate_on_submit():
        return redirect(url_for('index'))
    
    return render_template('login.html', title='Login', login_form=login_form, register_form=register_form)

# If a user wants to go to /register we should redirect them to /login
@app.route('/register')
def register():
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/documentation')
def documentation():
    return render_template('documentation.html', title='Documentation')