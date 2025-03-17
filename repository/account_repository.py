from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
from functions import write_logs
from login_manage import UserMixin
from models.account import Account, db
from .ParentAccess import ModelAccess


class AccountAccess(ModelAccess, UserMixin):

    @staticmethod
    @write_logs
    def create_account(name, password):
        password_hashed = generate_password_hash(password)
        if AccountAccess.is_account_name_unique(name):
            return ModelAccess.write_to_db(Account, name=name, password=password_hashed)
        return False

    @staticmethod
    @write_logs
    def is_already_followed(follower_account, following_account):
        return following_account.followers.filter_by(id=follower_account.id).first() is True


    @staticmethod
    @write_logs
    def is_following_to_self(follower_account, following_account):
        if follower_account == following_account:
            return True
        return False


    @staticmethod
    @write_logs
    def unfollow_from_account(unfollower_account, following_account):
        unfollower_account.following_to.remove(following_account)


    @staticmethod
    @write_logs
    def follow_to_account(follower_account, following_account):
        if not AccountAccess.is_already_followed(follower_account, following_account):
            print('not followed got')
            if not AccountAccess.is_following_to_self(follower_account, following_account):
                follower_account.following_to.append(following_account)
        else:
            print('already followed got')
            AccountAccess.unfollow_from_account(follower_account, following_account)


    @staticmethod
    @write_logs
    def verify_user_by_password(orig_user, password):
        return True if check_password_hash(orig_user.password, password) else False

    @staticmethod
    @write_logs
    def is_account_name_unique(account_name):
        return db.session.query(Account).filter_by(name=account_name).first() is None