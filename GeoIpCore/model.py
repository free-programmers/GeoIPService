import uuid
import datetime

from GeoIpCore.extensions import db
from sqlalchemy import Column, String, DateTime, Integer


class BaseTable(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True)

    def SetPubicKey(self):
        while True:
            key = str(uuid.uuid4())
            db_res = self.query.filter(self.PublicKey == key).first()
            if db_res:
                continue
            else:
                self.PublicKey = key
                break

    PublicKey = Column(String(36), nullable=False, unique=True)
    CreatedTime = Column(DateTime, default=datetime.datetime.now)
    LastUpdateTime = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
