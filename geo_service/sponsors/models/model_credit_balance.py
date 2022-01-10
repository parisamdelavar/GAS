from geo_service.database import BaseModel
from geo_service import db
from . import model_sponsor


class CreditBalance(BaseModel):
    __tablename__ = 'credit_balances'
    last_balance = db.Column(db.BigInteger, nullable=False)
    new_balance = db.Column(db.BigInteger, nullable=False)
    credit_amount = db.Column(db.BigInteger, nullable=False)
    log_date = db.Column(db.DateTime, nullable=False)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsors.id'))
    Sponsor = db.relationship('Sponsor', back_populates='credit_balance', lazy=True)
    # sponsor = db.relationship('Sponsor', back_populates='credit_type', lazy=True)
    Scenario_id = db.Column(db.Integer, nullable=False)
    Schedule_id = db.Column(db.Integer, nullable=False)
    sponsor_credit_type = db.Column(db.String)
    description = db.Column(db.String)

    def __repr__(self):
        return f' {self.__class__.__name__}({self.id}) '

