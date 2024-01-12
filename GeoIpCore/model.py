import uuid
import datetime

from .extensions import db
from GeoIpConfig.setting import DATABASE_TABLE_PREFIX_NAME
from sqlalchemy import String, DateTime, Integer, Column

from flask import current_app


class BaseModel(db.Model):
    """
    Base model class for all models
    """
    __abstract__ = True

    id = Column(Integer, primary_key=True)

    @staticmethod
    def SetTableName(name):
        """Use This Method For setting a table name"""
        name = name.replace("-", "_").replace(" ", "")

        return f"{DATABASE_TABLE_PREFIX_NAME}{name}"

    def SetPublicKey(self):
        """This Method Set a Unique PublicKey """
        while True:
            token = str(uuid.uuid4())
            if self.query.filter(self.PublicKey == token).first():
                continue
            else:
                self.PublicKey = token
                break

    PublicKey = Column(String(36), nullable=False, unique=True)
    CreatedTime = Column(DateTime, default=datetime.datetime.utcnow)
    LastUpdateTime = Column(DateTime, onupdate=datetime.datetime.utcnow, default=datetime.datetime.utcnow)

    def save(self):
        """
         combination of two steps, add and commit session
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(exc_info=e)
            return False
        else:
            return True
