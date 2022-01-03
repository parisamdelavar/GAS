from geo_service.database import BaseModel
from geo_service.extentions import db
from geo_service.sponsors.models import model_sponsor
from .modell_notification_type import Notification_Type
from geo_service.scenarios.models import modell_notification_type, model_scenario_type, model_scenario_calender, model_location, model_ran_schedule, model_affected_user
from geo_service.sponsors.models import model_sponsor
import uuid


def generate_uuid():
    return str(uuid.uuid4())


class Scenario(BaseModel):
    __tablename__ = 'scenarios'
    priority = db.Column(db.Integer, nullable=False)
    public_id = db.Column(db.String, name="public_id", default=generate_uuid)
    name = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    message = db.Column(db.String(200), nullable=False)
    prefix = db.Column(db.String(15), nullable=True)
    create_date = db.Column(db.DateTime, nullable=False)
    sender_number = db.Column(db.String(15), nullable=False)
    sender_user = db.Column(db.String(20), nullable=False)
    sender_pass = db.Column(db.String(20), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    delay = db.Column(db.BigInteger, nullable=False)
    location_limit = db.Column(db.Integer, nullable=False)
    last_modify_date = db.Column(db.DateTime, nullable=False)
    #max_location = db.Column(db.Integer, nullable=False)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsors.public_id'))
    notification_type_id = db.Column(db.Integer, db.ForeignKey('notification_types.id'))
    scenario_type_id = db.Column(db.Integer, db.ForeignKey('scenario_types.id'))
    sponsor = db.relationship('Sponsor', back_populates='scenario')
    location = db.relationship('Location', back_populates='scenario', lazy=True)
    scenario_calender = db.relationship('Scenario_Calender', back_populates='scenario', lazy=True)
    scenario_type = db.relationship('Scenario_Type', back_populates='scenario')
    notification_type = db.relationship('Notification_Type', back_populates='scenario')
    ran_schedules = db.relationship('Ran_Schedule', back_populates='scenario', lazy=True)


    def __repr__(self):
        return f' {self.__class__.__name__}({self.id},{self.name}) '


