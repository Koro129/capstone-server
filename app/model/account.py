from app import db
from datetime import datetime

class Account(db.Model):
    idAccount = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Account {}>'.format(self.name)