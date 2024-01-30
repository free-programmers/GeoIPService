from GeoIpCore.model import BaseModel
from sqlalchemy import Column, String


class ContactUS(BaseModel):
    """  """
    __tablename__ = BaseModel.SetTableName("ContactUs")

    Title = Column(String(255), nullable=False, unique=False)
    Email = Column(String(255), nullable=False, unique=False)
    Message = Column(String(2048), nullable=False, unique=False)