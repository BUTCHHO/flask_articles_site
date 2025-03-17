from sqlalchemy.exc import PendingRollbackError

from models import db


def rollback(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except PendingRollbackError:
            db.session.rollback()
            result = func(*args, **kwargs)
            return result
    return wrapper