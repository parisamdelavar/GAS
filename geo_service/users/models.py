from geo_service.database import BaseModel
from geo_service.sponsors.models import model_sponsor
from geo_service import db
import uuid


def generate_uuid():
    return str(uuid.uuid4())


association_table = db.Table('user_role_association', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)


class User(BaseModel):
    __tablename__ = 'users'
    username = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    public_id = db.Column(db.String, name="public_id", default=generate_uuid)
    roles = db.relationship('Role', secondary=association_table)
    sponsor = db.relationship('Sponsor', back_populates='user', lazy=True)

    def __repr__(self):
        return f' {self.__class__.__name__}({self.id},{self.username}) '




class Role(BaseModel):
    __tablename__ = 'roles'
    role_name = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(60), nullable=False)
    # users = db.relationship('UserRole', back_populates='roles', lazy=True)

    def __repr__(self):
        return f' {self.__class__.__name__}({self.id},{self.role_name}) '



