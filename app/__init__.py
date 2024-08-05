"""
Init File for pasted.sh app.
"""

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

# If the basedir for pasted.sh doesn't exist, make it.
if os.path.exists(Config.BASEDIR) is False:
    try:
        os.mkdir(Config.BASEDIR) # Root may be required depending on the path.
    except OSError as e:
        print(f'Error: {e}')
        exit()

from app import routes, models
