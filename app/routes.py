from werkzeug.datastructures import FileStorage
from flask import render_template, redirect, url_for, request, flash, Response, make_response
from flask_login import current_user, logout_user, login_user, login_required
import os
import datetime
from app import app, db, Config, csrf
from app.models import User, Files, ShortURL
from app.forms import LoginForm, RegistrationForm
import magic
import sqlalchemy as sa
import random
import mimetypes
import time
import sys
from io import BytesIO

@csrf.exempt # For cURL
@app.route('/', methods=["GET", "POST"])
def index():
    """General base for everything in the site.
    """
    if request.method == "GET":
        # Initial data for the index page
        hex_rand: str = os.urandom(15).hex()
        timestamp: int = int(datetime.datetime.now().timestamp())
        return render_template('index.html', title='Anonymous, Private, Secure, and Temporary.', hex_rand=hex_rand, timestamp=timestamp, user="", description=True)

    elif request.method == "POST":
        # Maybe check if this is a file or a url request.
        if request.form.get('file') or request.files['file'] is not None:
            # If this try except fails then the data is inside of the form rather than a file.
            try:
                data = request.files['file']
                mime: str = magic.from_buffer(data.read(1024), mime=True) # This will be needed when loading the file in browser.
                data.seek(0)
            except KeyError: # If its not a file, then itll just be a string.
                data = FileStorage(BytesIO(request.form.get('file').encode("UTF-8"))) # Just toss the stuff from the form into data instead
                mime: str = "text/plain"

            # Are we authenticated or not? Check current_user or fields from ther request
            if current_user.is_authenticated:
                owner_id = current_user.id
            elif request.form.get('user') and request.form.get('pass'):
                # Perform checks to see if this is the correct information
                user = User.query.filter_by(username=request.form.get('user')).first()
                if user is None or not user.pass_check(request.form.get('pass')):
                    return Response(f"[{request.host}] Invalid Credentials", status=401)
                owner_id = user.id # We can safely say the user is authenticated now.
            else:
                owner_id = None # User is unauthenticated, no probs.

            # We'll nab the filesize
            data.seek(0, os.SEEK_END)
            size = round(float(data.tell()) / (1024 * 1024), 2)
            size = request.content_length
            data.seek(0)

            # Get the user level of the person who owns the file
            if owner_id is not None:
                user = User.query.filter_by(id=owner_id).first()
                if user is not None:
                    user_level = user.level
                else:
                    user_level = 1

            # Check if the file is too large (for free users)
            if size > 256 * 1024 * 1024 and user_level < 2:
                return Response(f"[{request.host}] File too large\n", status=413)

            timestamp = time.time()

            # We'll also calculate retention for later
            retention = round(Config.MIN_EXPIRE + (-Config.MAX_EXPIRE + Config.MIN_EXPIRE) * pow((size / Config.MAX_CONTENT_LENGTH - 1), 3))

            # Lets get the expiry time
            if request.form.get('expiry'):
                # Check if provided expiry is more than calculated, if not, then we can use the provided one
                expiry = round(int(request.form.get('expiry')) + timestamp) if round(int(request.form.get('expiry')) + timestamp) < retention + timestamp else retention + timestamp
            else:
                # We calculate it from the file size in this instance
                expiry = retention + timestamp

            # See if a name was given for the file, if not then just generate a random one
            if request.form.get('name'):
                # Check if the name already exists
                if Files.query.filter_by(name=request.form.get('name')).first() is not None:
                    return Response(f"[{request.host}] Name already exists, please choose another.\n", status=409)
                name = request.form.get('name')
            else:
                name = ''.join(random.sample(Config.ALLOWED_CHARS, 4))
            hex_rand = os.urandom(15).hex()

            file = Files(
                name=name,
                size=sys.getsizeof(data),
                ext=mimetypes.guess_extension(mime),
                mime=mime,
                timestamp=timestamp,
                mgmt=hex_rand,
                expiry=expiry,
                domain=request.host,
                owner_id=owner_id
                )

            # Save data to storage
            data.save(f'{Config.BASEDIR}/{name}.{mimetypes.guess_extension(mime)}')

            # Finalise DB Writing
            try:
                db.session.add(file)
                db.session.commit()

                response = make_response(f"http://{request.host}/{name}{mimetypes.guess_extension(mime)}\n")
                response.headers["X-Expires"] = expiry
                response.headers["X-Token"] = hex_rand
                return response

            except Exception as e:
                db.session.rollback()
                print(e)
                return Response(f"[{request.host}] Internal Server Error, please try again or contact admin if urgent.\n", status=500)
        elif request.form.get('url'):
            data = request.form.get('url')

            # Are we authenticated or not? Check current_user or fields from ther request
            if current_user.is_authenticated:
                owner_id = current_user.id
            elif request.form.get('user') and request.form.get('pass'):
                # Perform checks to see if this is the correct information
                user = User.query.filter_by(username=request.form.get('user')).first()
                if user is None or not user.pass_check(request.form.get('pass')):
                    return Response(f"[{request.host}] Invalid Credentials", status=401)
                owner_id = user.id # We can safely say the user is authenticated now.
            else:
                owner_id = None # User is unauthenticated, no probs.

            # Get the user level of the person who owns the file
            if owner_id is not None:
                user = User.query.filter_by(id=owner_id).first()
                if user is not None:
                    user_level = user.level
                else:
                    user_level = 1

        else:
            return Response(f"[{request.host}] Invalid request\n", status=400)

@app.route('/<id>.<ext>')
def load(id, ext):
    """Handles the loading of everything in the app

    Args:
        id (str): The ID of the file you want to load.
        ext (str): The file extension.

    """

    # Get the file from the database
    file = db.session.scalar(sa.select(Files).where(Files.name == id and Files.ext == ext))

    # Check if the file exists
    if file is None:
        return Response(f"[{request.host}] File not found\n", status=404)

    # Open the file
    with open(f'{Config.BASEDIR}/{file.name}.{file.ext}', 'rb') as f:
        return Response(f.read(), mimetype=file.mime)

@app.route('/<id>.<ext>/delete', methods=["POST"])
def delete(id, ext):
    """Handles the deletion of files.

    Args:
        id (str): The ID of the file you want to delete.
        ext (str): The file extension.

    """

    # Check if mgmt token is provided
    token = request.form.get("token")
    if token is None:
        return Response("No token provided", status=400)

    # Lets look for the db entry
    file = db.session.scalar(sa.select(Files).where(Files.name == id and Files.ext == ext))
    if file is None:
        return Response(f"[{request.host}] File not found\n", status=404)

    # Does the token match what is in the db?
    if file.mgmt != token:
        return Response(f"[{request.host}] Invalid Token\n", status=403)

    # Delete the file
    # I'll do db first
    try:
        db.session.delete(file)
        os.remove(f'{Config.BASEDIR}/{file.name}.{file.ext}')
        db.session.commit()
        return Response(f"[{request.host}] File deleted\n", status=200)
    except Exception as e:
        db.session.rollback()
        print(e)
        return Response(f"[{request.host}] Internal Server Error, please try again or contact admin if urgent.\n", status=500)
    
@app.route('/paste', methods=["GET", "POST"])
def paste():
    """
    Route for the front-end uplaod page.
    """
    
    if request.method == "POST":
        return Response(f"[{request.host}] This is not an endpoint for terminal uploads, this is used for front-end uploading.\n", status=405)
    else:
        return render_template('paste.html', title='Upload', user="")
   
@app.route('/login', methods=["GET", "POST"])
def login():
    return "placeholder"

@app.route('/documentation')
def documentation():
    return render_template('documentation.html', title='Documentation')
