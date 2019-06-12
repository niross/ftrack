from datetime import datetime

from sqlalchemy import event

from app import db
from app.users import User
from app.ynab.models import YNABTransaction


class StarlingTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_locally = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    amount = db.Column(db.Integer)
    transaction_uid = db.Column(db.String(255), unique=True)
    transaction_type = db.Column(db.String(50))
    payee = db.Column(db.String(255), nullable=True)
    transaction_date = db.Column(db.DateTime())
    counter_party = db.Column(db.String(255), nullable=True)

    def update(self, data):
        for k, v in data.items():
            setattr(self, k, v)


@event.listens_for(StarlingTransaction, 'after_insert')
def receive_after_insert(mapper, connection, target):
    user = User.query.get(target.user_id)
    yt = YNABTransaction(
        starling_transaction=target.id,
        account_id=user.ynab_account_id,
        amount=target.amount,
        category_id=user.ynab_category_id,
        date=target.transaction_date,
        payee_name=target.counter_party
    )
    db.session.add(yt)


@event.listens_for(StarlingTransaction, 'after_update')
def receive_after_update(mapper, connection, target):
    yt = YNABTransaction.query.filter_by(starling_transaction=target.id).first()
    yt.update({
        'amount': target.amount,
        'date': target.transaction_date,
        'payee_name': target.counter_party,
    })
    db.session.merge(yt)

