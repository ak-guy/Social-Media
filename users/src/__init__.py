from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = 'project.db'

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    create_db(app)

    return app

def create_db(app):
    print(path)
    if not path.exists('/users/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')