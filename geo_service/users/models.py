from geo_service.database import BaseModel
from geo_service import db
import uuid


def generate_uuid():
    return str(uuid.uuid4())


class User(BaseModel):
    __tablename__ = 'users'
    username = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    public_id = db.Column(db.String, name="public_id", default=generate_uuid)
    user_role = db.relationship('UserRole', back_populates='users', lazy=True)

    def __repr__(self):
        return f' {self.__class__.__name__}({self.id},{self.username}) '


class UserRole(BaseModel):
    __tablename__ = 'user_roles'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='user_roles', lazy=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    role = db.relationship('Role', back_populates='role_users', lazy=True)

    def __repr__(self):
        return f' {self.__class__.__name__}({self.id}) '


class Role(BaseModel):
    __tablename__ = 'roles'
    role_name = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(60), nullable=False)
    user_role = db.relationship('UserRole', back_populates='roles', lazy=True)

    def __repr__(self):
        return f' {self.__class__.__name__}({self.id},{self.role_name}) '



