from app import app
from flask import render_template

@app.route('/')
def index():
    return render_template('index.html', title='Anonymous, Private, Secure, and Temporary.')

@app.route('/login')
def login():
    return render_template('login.html', title='Login')