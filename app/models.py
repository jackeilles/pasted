from typing import Optional
import sqlalchemy as sa
from sqlalchemy.orm import so 
from app import db
from flask_login import UserMixin
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(20), index=True, unique=True)
    password_hash = so.mapped_column(sa.String(128))

class Files(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    filename: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    mimetype: so.Mapped[str] = so.mapped_column(sa.String(16))
    

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))