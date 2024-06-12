from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
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
    timestamp: so.Mapped[datetime.datetime] = so.mapped_column(sa.DateTime, default=datetime.datetime.now)
    owner_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('user.id'))
    
class ShortURL(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    url: so.Mapped[str] = so.mapped_column(sa.String(128), index=True, unique=True)
    short: so.Mapped[str] = so.mapped_column(sa.String(8), index=True, unique=True)
    created: so.Mapped[datetime.datetime] = so.mapped_column(sa.DateTime, default=datetime.datetime.now)
    owner_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('user.id'))

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))