import os

from setting.database import db
from app import app


def init_db():
    os.remove('test.db')

    with app.test_request_context():
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        db.init_app(app)
        db.create_all()
