from types import NoneType

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
login_manager = LoginManager()
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(30), nullable = False)
    content = db.Column(db.Text(300), nullable = False)

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def create_article(cls,form):
        title = form['title']
        content = form['title']
        if title and content:
            article = cls(title=title, content=content)
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