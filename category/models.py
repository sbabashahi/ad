from setting.database import db
from utils.model import BaseModel


class Category(BaseModel):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __str__(self):
        return ''.join(['Cat: ', self.name])
