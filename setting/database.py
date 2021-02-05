from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def initialize_db(app):
    global db
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ad.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://flask:1234@mysql:3306/flask_db'
    db = SQLAlchemy(app)
    return db
