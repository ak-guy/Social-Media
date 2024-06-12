from src import db
from datetime import datetime

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    is_logged_in = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_staff = db.Column(db.Boolean, default=False)
    created_on = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self) -> dict:
        return f'User(id={self.id}, name={self.name}, username={self.username}, email={self.email}, created_on={self.created_on})'
