# from geo_service.database import BaseModel
# from geo_service.extentions import db
# from . import model_scenario
#
# class Ran_Schedule(BaseModel):
#     __tablename__ = 'ran_schedules'
#     date = db.Column(db.DateTime, nullable=False)
#     Message = db.Column(db.String(200), nullable=False)
#     status = db.Column(db.Integer, nullable=False)
#     scenario_id = db.Column(db.Integer, db.ForeignKey('scenarios.id'))
#     sponsors = db.relationship('Scenarios', back_populates='Locations', lazy=True)
#
#     def __repr__(self):
#         return f' {self.__class__.__name__}({self.id},{self.name}) '
#
#
