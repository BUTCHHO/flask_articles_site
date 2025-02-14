from types import NoneType

from datetime import datetime
from sqlalchemy import event
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
login_manager = LoginManager()

likes = db.Table('likes',
    db.Column('account_id', db.Integer, db.ForeignKey('account.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(30), nullable = False)
    content = db.Column(db.Text(300), nullable = False)
    likes = db.Column(db.Integer, default=0)
    author_id = db.Column(db.String(), db.ForeignKey('account.id'))
    creation_date = db.Column(db.String(), nullable = False)


    @classmethod
    def like_post(cls, request, user):
        liked_article_id = request["liked_article_id"]
        article = cls.query.get(liked_article_id)
        if article not in user.liked_posts:
            print('not in')
            user.liked_posts.append(article)
            article.likes = len(article.liked_by.all())
            db.session.commit()


    @classmethod
    def delete_all(cls):
        db.session.query(cls).delete()
        db.session.commit()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def create_article(cls,form, user):
        title = form['title']
        content = form['content']
        if title and content:
            creation_date = f"{datetime.now().day}/{datetime.now().month}/{datetime.now().year}"
            article = cls(title=title, content=content, author=user, creation_date=creation_date)
            try:
                db.session.add(article)
                db.session.commit()
            except Exception as err:
                print(err)
                return None
            return True
        return False

class Account(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False, unique=True)
    password = db.Column(db.String(256), nullable = False)
    posts = db.relationship('Post', backref='author')
    liked_posts = db.relationship('Post', secondary=likes, backref=db.backref('liked_by', lazy='dynamic'))


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
                print(err)
                return None
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

@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(user_id)


try:
    @event.listens_for(Post.liked_by, 'append')
    def update_likes_on_append(target):
        target.likes = len(target.liked_by)

    @event.listens_for(Post.liked_by, 'remove')
    def update_likes_on_remove(target):
        target.likes = len(target.liked_by)
except AttributeError:
    print('attr error')