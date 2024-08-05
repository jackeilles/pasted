from typing import Optional
from app import db, login, Config
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import os
import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True, unique=True)
    pass_h = db.Column(db.String)
    banned = db.Column(db.Boolean)
    ban_end = db.Column(db.DateTime)
    created = db.Column(db.DateTime)
    last_used = db.Column(db.DateTime)
    level = db.Column(db.Integer) # 1 = User, 2 = Paid, 3 = Root

    def __repr__(self):
        return f'<User {self.username}>'

    def pass_set(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def pass_check(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True, unique=True)
    size = db.Column(db.Integer)
    ext = db.Column(db.String, index=True, unique=True) # If not specified, it will be the same as name.
    mime = db.Column(db.String, index=True)
    timestamp = db.Column(db.DateTime)
    expiry = db.Column(db.DateTime)
    domain = db.Column(db.String, index=True)
    deleted = db.Column(db.Boolean, default=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f'<File {self.name}>'

    def del_file(self) -> str: # Only to be called when you're sure that a user is authenticated.
        """
        Deletes file from fs and blanks out db entry
        """

        if not self.name:
            raise ValueError("This file name doesn't exist. It might've already been deleted.")

        path = os.path.join(Config.FILE_PATH, self.name + self.ext)

        try:
            if os.path.exists(path): # make sure the file is actually there incase it's somehow slipped through the cracks.
                os.remove(path)

                # We should also update the database to reflect the deletion of the file.
                self.deleted = True
                self.name = None
                self.ext = None
                db.session.commit()
                return "File deleted successfully."
            else: # If this is somehow reached, it means that the file isn't in our fs, but is in the db for some reason, we should completely clear it.
                db.session.delete(self)
                db.session.commit()
                return "This file doesn't exist at all, was probably manually removed. Removing database entry."
        except Exception as e:
            db.session.rollback()
            return f"Error: {e}"

    def ban_owner(self, end: Optional[datetime.datetime] = None) -> str:
        """
        Bans the owner of the file.
        To be used in the event of a bad file being uploaded.
        """
        try:
            self.owner_id.banned = True
            self.owner_id.ban_end = end
            db.session.commit()
            return f"User {self.owner_id.username} banned successfully."
        except Exception as e:
            db.session.rollback()
            return f"Error: {e}"

class ShortURL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, index=True, unique=True)
    ext = db.Column(db.String, index=True, unique=True)
    timestamp = db.Column(db.DateTime)
    expiry = db.Column(db.DateTime)
    domain = db.Column(db.String, index=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f'<ShortURL {self.url}>'

    def del_url(self) -> str:
        """
        Deletes the short url from the database.
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return "Short URL deleted successfully."
        except Exception as e:
            db.session.rollback()
            return f"Error: {e}"

    def ban_owner(self, end: Optional[datetime.datetime] = None) -> str:
        """
        Bans the owner of the short url.
        To be used in the event of a bad short url being created.
        """
        try:
            self.owner_id.banned = True
            self.owner_id.ban_end = end
            db.session.commit()
            return f"User {self.owner_id.username} banned successfully."
        except Exception as e:
            db.session.rollback()
            return f"Error: {e}"

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
