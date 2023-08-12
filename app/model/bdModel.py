from datetime import datetime
from app import db

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(50), db.ForeignKey('config.uid', ondelete="CASCADE"), nullable=False)
    data = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<sensorData {self.id}>"

class Config(db.Model):
    uid = db.Column(db.String(50), primary_key=True)
    model = db.Column(db.String(50), nullable=False)
    ip = db.Column(db.String(50), nullable=False)
    setting = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<config {self.uid}>"