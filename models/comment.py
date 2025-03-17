from datetime import datetime
from .db import db

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    content = db.Column(db.String(500), nullable=False)
    likes = db.Column(db.Integer, default=0)
    author_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    creation_date = db.Column(db.String(), default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))