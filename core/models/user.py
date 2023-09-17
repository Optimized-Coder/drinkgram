from ..extensions import db
from flask_login import UserMixin, current_user

from .like import Like
from .photo import Photo
from .comment import Comment

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
    followers = db.relationship('User', secondary='followers',
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('following', lazy='dynamic'),
                               lazy='dynamic')
    def __repr__(self):
        return f'User {self.username}'

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
        
    def like_photo(self, photo_id):
        photo = Photo.query.filter_by(id=photo_id).first()
        existing_like = Like.query.filter_by(user_id=current_user.id, photo_id=photo_id).first()
        if existing_like:
        # User already liked the photo, so unlike it
            db.session.delete(existing_like)
            db.session.commit()
        
        else:
            new_like = Like(user_id=current_user.id, photo_id=photo_id)
            db.session.add(new_like)
            db.session.commit()
    def comment_photo(self, photo_id):
        new_comment = Comment(user_id=current_user.id, photo_id=photo_id)
        db.session.add(new_comment)
        db.session.commit()

    def follow_user(self, user_id):
        current_user.followers.append(user_id)
        db.session.commit()
    
    def unfollow_user(self, user_id):
        current_user.followers.remove(user_id)
        db.session.commit()

    @property
    def number_of_followers(self):
        return len(self.followers)
    
    