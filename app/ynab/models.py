from sqlalchemy import event

from app import db
from app.users import User
from app.ynab.api import YNABApi


class YNABTransaction(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    starling_transaction = db.Column(db.ForeignKey('starling_transaction.id'))
    account_id = db.Column(db.String(255))
    account_name = db.Column(db.String(255))
    amount = db.Column(db.Integer())
    category_id = db.Column(db.String(255), nullable=True)
    category_name = db.Column(db.String(255), nullable=True)
    date = db.Column(db.Date())
    ynab_id = db.Column(db.String(255), unique=True)
    memo = db.Column(db.String(255), nullable=True)
    payee_id = db.Column(db.String(255), nullable=True)
    payee_name = db.Column(db.String(255), nullable=True)

    def update(self, data):
        for k, v in data.items():
            setattr(self, k, v)


@event.listens_for(YNABTransaction, 'before_insert')
def receive_before_insert(mapper, connection, target):
    from app.starling.models import StarlingTransaction
    starling_trans = StarlingTransaction.query.get(
        target.starling_transaction
    )
    user = User.query.get(starling_trans.user_id)
    api = YNABApi(user)
    ynab_trans = api.create_transaction(
        target.amount * 1000,
        target.payee_name
    )
    target.ynab_id = ynab_trans['data']['transaction_ids'][0]


@event.listens_for(YNABTransaction, 'after_update')
def receive_after_update(mapper, connection, target):
    raise Exception('Transaction update')
