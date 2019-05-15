from datetime import datetime

from app import db


class StarlingTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_locally = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    amount = db.Column(db.Integer)
    transaction_uid = db.Column(db.String(255))
    type = db.Column(db.String(50))
