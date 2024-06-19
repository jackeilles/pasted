from werkzeug.datastructures import FileStorage
from flask import render_template, redirect, url_for, request
import os
import datetime
from app import app
from app.forms import LoginForm, RegistrationForm
import magic

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
            mime: str = magic.Magic(mime=True) # This will be needed when loading the file in browser.
        except KeyError:
            data: str = fdata['file'] # Just toss the stuff from the form into data instead
            mime: str = "text/plain"

        print(fdata)
        print(data)
        print(mime)

        return "Check term."

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