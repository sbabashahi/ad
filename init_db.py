from setting.database import db
from app import app


with app.test_request_context():
    db.init_app(app)
    db.create_all()
