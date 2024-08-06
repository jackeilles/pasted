from werkzeug.datastructures import FileStorage
from flask import render_template, redirect, url_for, request, flash, Response
from flask_login import current_user, logout_user, login_user, login_required
import os
import datetime
from app import app, db, Config
from app.models import User
from app.forms import LoginForm, RegistrationForm
from models import User, Files, ShortURL
import magic
import sqlalchemy as sa
import random
import mimetypes
import datetime
import sys

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

        # Maybe check if this is a file or a url request.
        if 'file' in fdata:
            # If this try except fails then the data is inside of the form rather than a file.
            try:
                data = request.files['file']
                data.seek(0)
                mime: str = magic.from_buffer(data.read(1024), mime=True) # This will be needed when loading the file in browser.
            except KeyError:
                data = fdata['file'] # Just toss the stuff from the form into data instead
                mime: str = "text/plain"

            # Lets upload it
            # Get the expiry
            expiry = Config.MIN_EXPIRE + (-Config.MAX_EXPIRE + Config.MIN_EXPIRE) * pow((sys.getsizeof(data) / Config.MAX_CONTENT_LENGTH - 1), 3)
            # Add to db first then save to fs
            rand = random.sample(Config.ALLOWED_CHARS, 4)
            file = Files(
                name=rand,
                size=sys.getsizeof(data),
                ext=mimetypes.guess_extension(mime),
                mime=mime,
                timestamp=datetime.datetime.now(),
                expiry=expiry,
                domain=request.host,
                owner_id=current_user.id if current_user.is_authenticated else None)

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
