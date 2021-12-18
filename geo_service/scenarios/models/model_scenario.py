from geo_service.database import BaseModel
from geo_service import db


class Scenario(BaseModel):

    __tablename__ = 'scenarios'
    name = db.Column(db.String(60), unique=True)

    def __repr__(self):
        return f' {self.__class__.__name__}({self.id},{self.name}) '



