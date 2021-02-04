import datetime
from hashlib import md5

import jwt
from setting.database import db
from utils.model import BaseModel
from utils.utils import create_jwt_secret


class User(BaseModel):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    secret = db.Column(db.String(50), default=create_jwt_secret)

    def set_password(self, raw_pass: str) -> str:
        self.password = self.hash_password(raw_pass)

    def check_password(self, raw_pass: str) -> bool:
        return True if self.password == self.hash_password(raw_pass) else False

    @staticmethod
    def hash_password(raw_pass: str) -> str:
        return md5(raw_pass.encode('utf-8')).hexdigest()

    def encode_auth_token(self):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=10),
                'iat': datetime.datetime.utcnow(),
                'sub': self.id,
            }
            return jwt.encode(
                payload,
                self.secret,
                algorithm='HS256'
            )
        except Exception as e:
            return e
