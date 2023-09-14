from ..extensions import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    photos = db.relationship('Photo', backref='user', lazy=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    about_me = db.Column(db.String(140))
    location = db.Column(db.String(140))

    @property
    def profile_complete(self):
        if self.first_name is None and self.last_name is None and self.location is None:
            return False
        else:
            return True