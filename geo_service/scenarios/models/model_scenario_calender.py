from geo_service.database import BaseModel
from geo_service.extentions import db
from . import model_scenario


class Scenario_Calender(BaseModel):
    __tablename__ = 'senario_calender'
    from_date = db.Column(db.DateTime, nullable=False)
    to_date = db.Column(db.DateTime, nullable=False)
    repeat = db.Column(db.String(20), nullable=False)
    from_time = db.Column(db.Time, nullable=False)
    to_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    province = db.Column(db.String(60), nullable=True)
    scenario_id = db.Column(db.Integer, db.ForeignKey('scenarios.id'))
    scenario = db.relationship('Scenario', back_populates='scenario_calender')

    def __repr__(self):
        return f' {self.__class__.__name__}({self.id},{self.name}) '


