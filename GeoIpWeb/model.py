from GeoIpCore.model import BaseTable
from sqlalchemy import Column, String


class ContactUS(BaseTable):
    __tablename__ = "ContactUs"

    Title = Column(String(255), nullable=False, unique=False)
    Email = Column(String(255), nullable=False, unique=False)
    Message = Column(String(512), nullable=False, unique=False)


