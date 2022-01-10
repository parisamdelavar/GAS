from geo_service.database import BaseModel
from geo_service.extentions import db
from . import model_scenario
import enum






class Location(BaseModel):
    __tablename__ = 'Locations'
    cell_id = db.Column(db.String(60), nullable=True)
    lac_id = db.Column(db.String(60), nullable=True)
    lat = db.Column(db.Float, nullable=True)
    long = db.Column(db.Float, nullable=True)
    distance = db.Column(db.Integer, nullable=True)
    status = db.Column(db.Boolean, nullable=False)
    city = db.Column(db.String(60), nullable=True)
    province = db.Column(db.String(60), nullable=True)
    scenario_id = db.Column(db.Integer, db.ForeignKey('scenarios.id'))
    scenario = db.relationship('Scenario', back_populates='location', lazy=True)
    location_type = db.relationship('Location_Type', back_populates='location')
    location_type_id = db.Column(db.Integer, db.ForeignKey('Location_types.id'))
    Lat_long_distance = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f' {self.__class__.__name__}({self.id},{self.name}) '



class Location_Type(BaseModel):
    __tablename__ = 'Location_types'
    name = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    location = db.relationship('Location', back_populates='location_type', lazy=True)

    def __repr__(self):
        return f' {self.__class__.__name__}({self.id},{self.name})'


