from sqlalchemy.ext.hybrid import hybrid_property

from .relations_tables import acc_likes_com, likes, acc_follows_acc
from flask_login import UserMixin

from .db import db

class Account(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False, unique=True)
    bio = db.Column(db.String(750), nullable=True)
    password = db.Column(db.String(256), nullable = False)
    posts = db.relationship('Post', backref='author')
    liked_posts = db.relationship('Post', secondary=likes, backref=db.backref('liked_by', lazy='dynamic'), lazy='dynamic', cascade='all, delete')
    comments = db.relationship('Comment', backref='author')
    liked_comments = db.relationship('Comment', secondary=acc_likes_com, backref=db.backref('liked_by', lazy='dynamic'), cascade='all, delete')
    following_to = db.relationship('Account', secondary=acc_follows_acc,
                                   primaryjoin=(id == acc_follows_acc.c.follower_id),
                                   secondaryjoin=(id == acc_follows_acc.c.followed_id),
                                   backref=db.backref('followers', lazy='dynamic'),
                                   lazy='dynamic',
                                   cascade='all, delete')

    @hybrid_property
    def followers_count(self):
        return self.followers.count()


    @hybrid_property
    def liked_posts_count(self):
        return self.liked_posts.count()

