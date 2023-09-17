from datetime import datetime
from ..extensions import db

from .like import Like
from .comment import Comment

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    url = db.Column(db.String(255))
    description = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    likes = db.relationship('Like', backref='photo', lazy='dynamic')
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


    @property
    def get_number_of_likes(self):
        return len(self.likes)
    
    @property
    def get_comments(self):
        return Comment.query.filter_by(photo_id=self.id).all()
    
