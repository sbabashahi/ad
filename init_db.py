from setting.database import db
from app import app


with app.test_request_context():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ad.db'
    db.init_app(app)
    db.create_all()
