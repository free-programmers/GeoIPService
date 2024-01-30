from sqlalchemy import Column, String

from GeoIpCore.model import BaseModel


class ContactUS(BaseModel):
    """  """
    __tablename__ = BaseModel.SetTableName("ContactUs")

    Title = Column(String(255), nullable=False, unique=False)
    Email = Column(String(255), nullable=False, unique=False)
    Message = Column(String(2048), nullable=False, unique=False)
