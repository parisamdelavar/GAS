from geo_service.database import BaseModel
from geo_service.extentions import db


class Scenario_Type(BaseModel):
    __tablename__ = 'scenario_types'
    name = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    scenario = db.relationship('scenario', back_populates='scenario_type', lazy=True)

    def __repr__(self):
        return f' {self.__class__.__name__}({self.id},{self.name}) '


