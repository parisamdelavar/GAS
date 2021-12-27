from geo_service.database import BaseModel
from geo_service import db
from . import model_sponsor


class CreditType(BaseModel):
    __tablename__ = 'credit_types'
    name = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(300), nullable=True)
    Sponsor = db.relationship('Sponsor', back_populates='credit_type', lazy=True)



    def __repr__(self):
        return f' {self.__class__.__name__}({self.id},{self.name}) '


