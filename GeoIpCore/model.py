# build in
import uuid
import datetime

# lib
from sqlalchemy import String, DateTime, Integer, Column


# app
from .extensions import db
from GeoIpConfig.setting import DATABASE_TABLE_PREFIX_NAME

# framwork
from flask import current_app


class BaseModel(db.Model):
    """ Base model class for all models in app"""
    __abstract__ = True

    id = Column(Integer, primary_key=True)

    @staticmethod
    def SetTableName(name:str) -> str:
        """Use This Method For setting a table name.
            this method normalize table name and then 
            added DATABASE TABLE PREFIX NAME to beginning of table name        
        """
        name = name.replace("-", "_").replace(" ", "")

        return f"{DATABASE_TABLE_PREFIX_NAME}{name}"

    def SetPublicKey(self) -> bool:
        """This Method Set a Unique PublicKey for each record -> uuid"""
        while True:
            token = str(uuid.uuid4())
            if self.query.filter(self.PublicKey == token).first():
                continue
            else:
                self.PublicKey = token
                return True
                

    PublicKey = Column(String(36), nullable=False, unique=True)
    CreatedTime = Column(DateTime, default=datetime.datetime.utcnow)
    LastUpdateTime = Column(DateTime, onupdate=datetime.datetime.utcnow, default=datetime.datetime.utcnow)

    def save(self) -> bool:
        """ combination of two steps, add and commit session
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
