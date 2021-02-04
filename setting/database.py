from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def initialize_db(app):
    global db
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    db = SQLAlchemy(app)
    return db

