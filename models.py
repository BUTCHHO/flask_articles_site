from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(30), nullable = False)
    content = db.Column(db.Text(300), nullable = False)

class Account(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False, unique=True)
    password = db.Column(db.String(256), nullable = False)


@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(user_id)