from geo_service.database import BaseModel
from geo_service import db


class Sponsor(BaseModel):
    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f' {self.__class__.__name__}({self.id},{self.name}) '




