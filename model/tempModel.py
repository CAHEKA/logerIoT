import os

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Config(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(50), unique=True)
    setting = db.Column(db.String(50), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<config {self.id}>"


