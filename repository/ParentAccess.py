from typing import Type

from functions import write_logs, rollback
from models import db


class ModelAccess:

    @staticmethod
    @write_logs
    def delete_all_records(model: Type[db.Model]):
        model.query.delete()
        db.session.commit()

    @staticmethod
    @write_logs
    def delete_record_by_id(model: Type[db.Model], object_id):
        model.query.filter_by(id=object_id).delete()
        db.session.commit()

    @staticmethod
    @write_logs
    def get_all_records(model: Type[db.Model]):
        return model.query.all()

    @staticmethod
    @write_logs
    def get_record_by_id(model: Type[db.Model], object_id):
        return model.query.filter_by(id=object_id).first()

    @staticmethod
    @write_logs
    def get_record_by(model: Type[db.Model], **kwargs):
        return model.query.filter_by(**kwargs).first()


    @staticmethod
    @write_logs
    def write_to_db(model: Type[db.Model], **kwargs):
        try:
            record = model(**kwargs)
            db.session.add(record)
            db.session.commit()
        except:
            db.session.rollback()
        return True



