from app import app
from app.forms import LoginForm, RegistrationForm
from flask import render_template, redirect, url_for
import os
import datetime

@app.route('/', methods=["GET", "POST"])
def index():
    # Initial data for the index page
    hex_rand: str = os.urandom(15).hex()
    timestamp: int = int(datetime.datetime.now().timestamp())

    return render_template('index.html', title='Anonymous, Private, Secure, and Temporary.', hex_rand=hex_rand, timestamp=timestamp)

@app.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    register_form = RegistrationForm()

    if login_form.validate_on_submit():
        return redirect(url_for('index'))
    
    if register_form.validate_on_submit():
        return redirect(url_for('index'))
    
    return render_template('login.html', title='Login', login_form=login_form, register_form=register_form)

@app.route('/documentation')
def documentation():
    return render_template('documentation.html', title='Documentation')