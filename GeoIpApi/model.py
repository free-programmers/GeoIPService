# build in
import json
import ipaddress

# apps
from GeoIpCore.model import BaseModel

# libs
from sqlalchemy import Column, String, BIGINT, JSON, DECIMAL


class BaseIPSerializer:

    def serialize(self, intip, ip):
        return {
            "CountryCode": self.CountryCode,
            "CountryName": self.CountryName,
            "StateName": self.StateName,
            "CityName": self.CityName,
            "latitude": self.Lat,
            "longitude": self.Long,
            "ZipCode": self.ZipCode,
            "TimeZone": self.TimeZone,
            "ip": {
                "oct": ip,
                "hex": hex(intip),
                "decimal": intip,
            }
        }


class BaseCOUNTRYSerializer:

    def serialize(self):
        return json.loads(self.Info)


class IPV4(BaseModel, BaseIPSerializer):
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

    def setStartRange(self, ip: str):
        self.StartRange = int(ipaddress.ip_address(ip))

    def setEndRange(self, ip: str):
        self.EndRange = int(ipaddress.ip_address(ip))


class IPV6(BaseModel, BaseIPSerializer):
    """This Class Contain Ipv6 range and name"""
    __tablename__ = BaseModel.SetTableName("IPV6")
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


class CountryInfo(BaseModel, BaseCOUNTRYSerializer):
    __tablename__ = BaseModel.SetTableName("CountryInfo")
    CommonName = Column(String(255), unique=False, nullable=False)
    OfficialName = Column(String(255), unique=False, nullable=False)
    CountryCode = Column(String(64), unique=False, nullable=False)
    Info = Column(JSON, unique=False, nullable=False)
