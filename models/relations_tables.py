from .db import db

likes = db.Table('likes',
    db.Column('account_id', db.Integer, db.ForeignKey('account.id', ondelete="CASCADE"), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), primary_key=True)
)

acc_likes_com = db.Table('acc_likes_com',
    db.Column('account_id', db.Integer, db.ForeignKey('account.id', ondelete='CASCADE'), primary_key=True),
    db.Column('comment_id', db.Integer, db.ForeignKey('comment.id', ondelete='CASCADE'), primary_key=True)
                         )

acc_follows_acc = db.Table('acc_follows_acc',
    db.Column('follower_id', db.Integer, db.ForeignKey('account.id', ondelete='CASCADE'), primary_key=True),
    db.Column('followed_id', db.Integer, db.ForeignKey('account.id', ondelete='CASCADE'), primary_key=True)
                           )