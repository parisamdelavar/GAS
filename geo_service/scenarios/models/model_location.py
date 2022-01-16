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
    area = db.Column(db.String(200), nullable=True)
    formatted_Location = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f' {self.__class__.__name__}({self.id},{self.name}) '


    def __init__(self):
        self.formatted_Location = format_lac_cell( self.lac_id, self.cell_id)

    def format_lac_cell(self):
        if 3 < len(self.cell_id) < 6:  # 2g 3g
            self.formatted_Location = str(self.lac_id) + "00" + str(self.cell_id)
        if 0 < len(self.cell_id) < 3:  # 4g
            self.formatted_Location = str(self.lac_id) + "00" + str(self.cell_id)


class Location_Type(BaseModel):
    __tablename__ = 'Location_types'
    name = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    location = db.relationship('Location', back_populates='location_type', lazy=True)

    def __repr__(self):
        return f' {self.__class__.__name__}({self.id},{self.name})'


def format_lac_cell(lac, cellid):
    if 3 < len(cellid) < 6:  # 2g 3g
        new = str(lac) + "00" + str(cellid)
    if 0 < len(cellid) < 3:  # 4g
        new = cellid
    return new


