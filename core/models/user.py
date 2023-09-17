from ..extensions import db
from flask_login import UserMixin

followers = db.Table('followers',
            db.Column('follower_id', db.Integer(), db.ForeignKey('user.id')),
            db.Column('followed_id', db.Integer(), db.ForeignKey('user.id'))
            )

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
    followers = db.relationship('User', backref='followers', lazy=True)

    @property
    def profile_complete(self):
        if self.first_name is None and self.last_name is None and self.location is None:
            return False
        else:
            return True
        
    @property
    def get_name(self):
        if self.first_name is None and self.last_name is None:
            return 'Unknown User'
        else:
            return f'{self.first_name} {self.last_name}'
        
