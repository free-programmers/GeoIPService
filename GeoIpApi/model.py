from GeoIpCore.model import BaseModel
from sqlalchemy import Column, String, BIGINT, JSON, DECIMAL


class IPV4(BaseModel):
    """This Class Contain Ipv4 range and name"""
    __tablename__ = BaseModel.SetTableName("IPV4")

    StartRange = Column(BIGINT, unique=False, nullable=False)
    EndRange = Column(BIGINT, nullable=False, unique=True)

    CountryCode = Column(String(64), unique=False, nullable=False)
    CountryName = Column(String(64), unique=False, nullable=False)
    StateName = Column(String(64), unique=False, nullable=False)
    CityName = Column(String(64), unique=False, nullable=False)
    Lat = Column(String(64), unique=False, nullable=False)
    Long = Column(String(64), unique=False, nullable=False)

    ZipCode = Column(String(64), nullable=False, unique=False)
    TimeZone = Column(String(64), unique=False, nullable=False)


class IPV6(BaseModel):
    """This Class Contain Ipv6 range and name"""
    __tablename__ = "IPV6"
    StartRange = Column(DECIMAL(scale=0, precision=36), unique=False, nullable=False)
    EndRange = Column(DECIMAL(scale=0, precision=36), nullable=False, unique=True)

    CountryCode = Column(String(64), unique=False, nullable=False)
    CountryName = Column(String(64), unique=False, nullable=False)
    StateName = Column(String(64), unique=False, nullable=False)
    CityName = Column(String(64), unique=False, nullable=False)
    Lat = Column(String(64), unique=False, nullable=False)
    Long = Column(String(64), unique=False, nullable=False)

    ZipCode = Column(String(64), nullable=False, unique=False)
    TimeZone = Column(String(64), unique=False, nullable=False)


class CountryInfo(BaseModel):
    __tablename__ = "CountryInfo"
    CommonName = Column(String(255), unique=False, nullable=False)
    OfficialName = Column(String(255), unique=False, nullable=False)
    CountryCode = Column(String(64), unique=False, nullable=False)
    Info = Column(JSON, unique=False, nullable=False)
