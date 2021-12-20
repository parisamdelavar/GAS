from geo_service.database import BaseModel
from geo_service import db
from . import model_sponsor
import uuid


def generate_uuid():
    return str(uuid.uuid4())


class Senario(BaseModel):
    __tablename__ = 'scenarios'
    priority = db.Column(db.Integer, nullable=False)
    public_id = db.Column(db.String, name="public_id", default=generate_uuid)
    name = db.Column(db.string(60), nullable=False)
    description = db.Column(db.string(200), nullable=True)
    message = db.Column(db.string(200), nullable=False)
    prefix = db.Column(db.string(15), nullable=True)
    create_date = db.Column(db.Datetime, nullable=False)
    sender_number = db.Column(db.string(15), nullable=False)
    sender_user = db.Column(db.string(20), nullable=False)
    sender_pass = db.Column(db.string(20), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    delay = db.Column(db.BigInteger, nullable=False)
    location_limit = db.Column(db.Integer, nullable=False)
    max_location = db.Column(db.Integer, nullable=False)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsors.id'))
    notification_type = db.Column(db.Integer, db.ForeignKey('notification_types.id'))
    type = db.Column(db.Integer, db.ForeignKey('scenario_types.id'))
    sponsor = db.relationship('Sponsor', back_populates='scenario', lazy=True)
    location = db.relationship('Location', back_populates='scenario')
    scenario_calender = db.relationship('Scenario_Calender', back_populates='scenario')
    scenario_type = db.relationship('Scenario_Type', back_populates='scenario', lazy=True)
    notification = db.relationship('Notification_Type', back_populates='scenario', lazy=True)
    ran_schedules = db.relationship('Ran_Schedule', back_populates='scenario')


    def __repr__(self):
        return f' {self.__class__.__name__}({self.id},{self.name}) '


