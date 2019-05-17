from app import db


class YNABTransaction(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    account_id = db.Column(db.String(255))
    account_name = db.Column(db.String(255))
    amount = db.Column(db.Integer())
    approved = db.Column(db.Boolean)
    category_id = db.Column(db.String(255), nullable=True)
    category_name = db.Column(db.String(255), nullable=True)
    date = db.Column(db.Date())
    ynab_id = db.Column(db.String(255), unique=True)
    memo = db.Column(db.String(255), nullable=True)
    payee_id = db.Column(db.String(255), nullable=True)
    payee_name = db.Column(db.String(255), nullable=True)

