from GeoIpCore.model import BaseModel
from GeoIpCore.extensions import db
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash

AdminsPermission = db.Table(
    BaseModel.SetTableName("admins-permission"),
    Column("AdminID", ForeignKey(BaseModel.SetTableName("admins") + ".id")),
    Column("PermissionID", ForeignKey(BaseModel.SetTableName("permissions") + ".id"))
)


class Admin(BaseModel):
    __tablename__ = BaseModel.SetTableName("admins")

    Username = Column(String(256), unique=True, nullable=False)
    Password = Column(String(102), unique=False, nullable=False)
    Email = Column(String(512), unique=True, nullable=False)
    PhoneNumber = Column(String(11), unique=True, nullable=False)
    Active = Column(Boolean, default=False)
    TryNumber = Column(Integer, default=0)

    Permissions = db.relationship("Permission", secondary=AdminsPermission, backref="Admin", lazy="dynamic")

    def setPassword(self, password: str) -> None:
        self.Password = generate_password_hash(password, method="scrypt")

    def checkPassword(self, password: str) -> bool:
        return check_password_hash(pwhash=self.Password, password=password)

    def setUsername(self, username: str) -> bool:
        if db.session.execute(db.select(self).filter_by(Username=username)).scalar_one_or_none():
            return False
        else:
            self.Username = username
            return True

    def setPhonenumber(self, phone: str) -> bool:
        if db.session.execute(db.select(self).filter_by(PhoneNumber=phone)).scalar_one_or_none():
            return False
        else:
            self.PhoneNumber = phone
            return True

    def setEmail(self, email: str) -> bool:
        if db.session.execute(db.select(self).filter_by(Email=email)).scalar_one_or_none():
            return False
        else:
            self.Email = email
            return True

    def setActivate(self):
        self.Active = True


class Permission(BaseModel):
    """
     Permission Handler Table

        backref=GetAdmin
    """
    __tablename__ = BaseModel.SetTableName("permissions")
    Description = Column(String(1024), unique=False, nullable=False)
    Permission = Column(String(256), unique=True, nullable=False)
