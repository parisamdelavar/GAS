from app.database import BaseModel
from app import db


class Scenario(BaseModel):
    name = db.Column(db.String(60), unique=True)

    def __repr__(self):
        return f' {self.__class__.__name__}({self.id},{self.name}) '


