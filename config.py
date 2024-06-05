import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'set-this-if-you-cant-use-env-vars'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    