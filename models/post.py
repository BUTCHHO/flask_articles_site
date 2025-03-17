from .db import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(30), nullable = False)
    content = db.Column(db.Text(300), nullable = False)
    likes = db.Column(db.Integer, default=0)
    author_id = db.Column(db.String(), db.ForeignKey('account.id'))
    creation_date = db.Column(db.String(), nullable = False)
    comments = db.relationship('Comment', backref='post', lazy=True)
