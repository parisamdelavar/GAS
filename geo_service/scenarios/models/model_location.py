from geo_service.database import BaseModel
from geo_service.extentions import db
from . import model_scenario
import enum


class location_type(enum.Enum):
    lac_cell = 1
    lat_long = 2



class Location(BaseModel):
    __tablename__ = 'Locations'
    cell_id = db.Column(db.String(60), nullable=True)
    lac_id = db.Column(db.String(60), nullable=True)
    lat = db.Column(db.Float, nullable=True)
    long = db.Column(db.Float, nullable=True)
    status = db.Column(db.Boolean, nullable=False)
    city = db.Column(db.String(60), nullable=True)
    province = db.Column(db.String(60), nullable=True)
    scenario_id = db.Column(db.Integer, db.ForeignKey('scenarios.id'))
    scenario = db.relationship('Scenario', back_populates='location', lazy=True)
    type = db.Column(db.Enum(location_type))

    def __repr__(self):
        return f' {self.__class__.__name__}({self.id},{self.name}) '

