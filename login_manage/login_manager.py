from flask_login import LoginManager
from models import Account

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(user_id)
