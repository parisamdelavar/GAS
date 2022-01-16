from geo_service.database import BaseModel
from geo_service import db
from . import model_credit_type
from geo_service.scenarios.models import model_scenario
from geo_service.users import models
import uuid



def generate_uuid():
    return str(uuid.uuid4())


class Sponsor(BaseModel):
    __tablename__ = 'sponsors'
    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    public_id = db.Column(db.String, name="public_id", default=generate_uuid)
    status = db.Column(db.Integer, default=1)
    credit_type_id = db.Column(db.Integer, db.ForeignKey('credit_types.id'))
    credit_type = db.relationship('CreditType', back_populates='sponsors')
    credit_balance = db.relationship('CreditBalance', back_populates='Sponsor')
    scenario = db.relationship('Scenario', back_populates='sponsor', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='sponsor')

    #credit_balance = db.relationship('CreditBalance', back_populates='sponsor')
    # scenario = db.relationship('Scenario', back_populates='sponsor', lazy=True)


    def __repr__(self):
        return f' {self.__class__.__name__}({self.id},{self.name}) '





