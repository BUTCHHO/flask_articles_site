from types import NoneType

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

from functions import today_date
from my_logging import write_logs


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

likes = db.Table('likes',
    db.Column('account_id', db.Integer, db.ForeignKey('account.id', ondelete="CASCADE"), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), primary_key=True)
)

acc_likes_com = db.Table('acc_likes_com',
    db.Column('account_id', db.Integer, db.ForeignKey('account.id', ondelete='CASCADE'), primary_key=True),
    db.Column('comment_id', db.Integer, db.ForeignKey('comment.id', ondelete='CASCADE'), primary_key=True)
                         )


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(30), nullable = False)
    content = db.Column(db.Text(300), nullable = False)
    likes = db.Column(db.Integer, default=0)
    author_id = db.Column(db.String(), db.ForeignKey('account.id'))
    creation_date = db.Column(db.String(), nullable = False)
    commentaries = db.relationship('Comment', backref='post', lazy=True)

    @classmethod
    @write_logs
    def like_post(cls, form, user):
        liked_article_id = form["liked_article_id"]
        article = cls.query.get(liked_article_id)
        try:
            if article not in user.liked_posts:
                user.liked_posts.append(article)
                article.likes = len(article.liked_by.all())
                db.session.commit()
            else:
                user.liked_posts.remove(article)
                article.likes = len(article.liked_by.all())
                db.session.commit()
        except Exception as err:
            return err


    @classmethod
    def delete_all(cls):
        db.session.query(cls).delete()
        db.session.commit()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    @write_logs
    def create_article(cls,form, user):
        title = form['title']
        content = form['content']
        if title and content:
            article = cls(title=title, content=content, author=user, creation_date=today_date())
            try:
                db.session.add(article)
                db.session.commit()
            except Exception as err:
                return err
            return True
        return False #если НЕ введён заголвок и содержание





class Account(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False, unique=True)
    password = db.Column(db.String(256), nullable = False)
    posts = db.relationship('Post', backref='author')
    liked_posts = db.relationship('Post', secondary=likes, backref=db.backref('liked_by', lazy='dynamic'), cascade='all, delete')
    commentaries = db.relationship('Comment', backref='author')
    liked_commentaries = db.relationship('Comment', secondary=acc_likes_com, backref=db.backref('liked_by', lazy='dynamic'), cascade='all, delete')


    @classmethod
    def delete_all(cls):
        db.session.query(cls).delete()
        db.session.commit()

    @classmethod
    def create_account(cls, form):
        name = form['name']
        password = form['password']
        if name and password:
            password_hashed = generate_password_hash(password)
            account = cls(name=name, password=password_hashed)
            try:
                db.session.add(account)
                db.session.commit()
            except Exception as err:
                return err
            return True
        return False

    @classmethod
    def verify_account(cls,form):
        name = form['name']
        password = form['password']
        if name and password:
            acc = cls.query.filter_by(name=name).first()
            if not (isinstance(acc, NoneType)) and check_password_hash(acc.password, password):
                return {"user": acc, "verified": True}
        return {"user": None, "verified": False}



class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable=False)
    content = db.Column(db.String(500), nullable=False)
    likes = db.Column(db.Integer, default=0)
    author_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    creation_date = db.Column(db.String(), default=today_date())

    @classmethod
    def create_commentary(cls,form, user, target_post):
        try:
            comment_content = form['write_comment']
            print(form, comment_content)
            if comment_content:
                comment = Comment(content=comment_content, author_id=user.id,post_id=target_post.id)
                target_post.commentaries.append(comment)
                db.session.commit()
                return True
            return False
        except Exception as err:
            return err

    @classmethod
    @write_logs
    def like_comment(cls, form, user):
        liked_comment_id = form['like_comment']
        liked_comment = cls.query.get(liked_comment_id)
        try:
            if liked_comment not in user.liked_commentaries:
                user.liked_commentaries.append(liked_comment)
                liked_comment.likes = len(liked_comment.liked_by.all())
                db.session.commit()
            else:
                user.liked_commentaries.remove(liked_comment)
                liked_comment.likes = len(liked_comment.liked_by.all())
                db.session.commit()
        except Exception as err:
            print('error (check logs)')
            return err


@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(user_id)
