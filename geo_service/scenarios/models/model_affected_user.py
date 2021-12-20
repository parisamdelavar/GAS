from geo_service.database import BaseModel
from geo_service import db
from . import model_ran_schedule


class Affected_User(BaseModel):
    __tablename__ = 'affected_users'
    date = db.Column(db.DateTime, nullable=False)
    Message = db.Column(db.String(200), nullable=False)
    status = db.Column(db.int, nullable=False)
    ran_scenario_id = db.Column(db.Integer, db.ForeignKey('ran_schedules.id'))
    ran_schedule = db.relationship('Ran_Schedule', back_populates='affected_user', lazy=True)

    def __repr__(self):
        return f' {self.__class__.__name__}({self.id},{self.name}) '


