from geo_service.database import BaseModel
from geo_service import db
from . import model_credit_type
import uuid


def generate_uuid():
    return str(uuid.uuid4())


class Sponsor(BaseModel):
    __tablename__ = 'sponsors'
    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    public_id = db.Column(db.String, name="public_id", default=generate_uuid)
    credit_type = db.Column(db.Integer, db.ForeignKey('credit_types.id'))
    credit = db.relationship('credit_types', back_populates='sponsors')


    def __repr__(self):
        return f' {self.__class__.__name__}({self.id},{self.name}) '




