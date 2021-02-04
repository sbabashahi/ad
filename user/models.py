from hashlib import md5

from setting.database import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def create(self):
        db.session.add(self)
        return self.save()

    def save(self):
        db.session.commit()
        return self

    def set_password(self, raw_pass: str) -> str:
        self.password = self.hash_password(raw_pass)

    def check_password(self, raw_pass: str) -> bool:
        return True if self.password == self.hash_password(raw_pass) else False

    @staticmethod
    def hash_password(raw_pass: str) -> str:
        return md5(raw_pass.encode('utf-8')).hexdigest()


def init_db():
    db.create_all()
