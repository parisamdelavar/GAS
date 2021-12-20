from geo_service.database import BaseModel
from geo_service import db
from . import model_senario


class Location(BaseModel):
    __tablename__ = 'Locations'
    cell_id = db.Column(db.String(60), nullable=False)
    lac_id = db.Column(db.String(60), nullable=False)
    status = db.Column(db.Bit, nullable=False)
    city = db.Column(db.String(60), nullable=True)
    province = db.Column(db.String(60), nullable=True)
    scenario_id = db.Column(db.Integer, db.ForeignKey('scenarios.id'))
    sponsors = db.relationship('Scenario', back_populates='location', lazy=True)

    def __repr__(self):
        return f' {self.__class__.__name__}({self.id},{self.name}) '

