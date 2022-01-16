from geo_service.database import BaseModel
from geo_service.extentions import db
from geo_service.scenarios.models import model_scenario


class Notification_Type(BaseModel):
    __tablename__ = 'notification_types'
    name = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    scenario = db.relationship('Scenario', back_populates='notification_type', lazy=True)

    def __repr__(self):
        return f' {self.__class__.__name__}({self.id},{self.name}) '



