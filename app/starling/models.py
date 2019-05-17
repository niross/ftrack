from datetime import datetime

from app import db


class StarlingTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_locally = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    amount = db.Column(db.Integer)
    transaction_uid = db.Column(db.String(255), unique=True)
    transaction_type = db.Column(db.String(50))
    payee = db.Column(db.String(255), nullable=True)

    def update(self, data):
        for k, v in data.items():
            setattr(self, k, v)
