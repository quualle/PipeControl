
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone = db.Column(db.String(50))
    email = db.Column(db.String(100))
    status = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_changed = db.Column(db.DateTime, nullable =False , default=datetime.utcnow)
    zugehoerigkeit = db.Column(db.String(50), nullable=True)
    notes = db.Column(db.Text, nullable=True)

    def __init__(self, first_name, last_name, phone, email, status, zugehoerigkeit):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.status = status
        self.created_at = datetime.utcnow()
        self.last_changed = datetime.utcnow()
        self.zugehoerigkeit = zugehoerigkeit


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add additional fields for customer


class Caregiver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add additional fields for caregiver
