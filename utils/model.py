from setting.database import db


class BaseModel(db.Model):
    __abstract__ = True

    def create(self):
        db.session.add(self)
        return self.save()

    def save(self):
        db.session.commit()
        return self
