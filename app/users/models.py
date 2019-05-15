import uuid

from flask_security import RoleMixin, UserMixin
from sqlalchemy import event

from app import db

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    ynab_auth_code = db.Column(db.String(255), nullable=True)
    uuid = db.Column(db.String(36), unique=True, nullable=True)
    starling_auth_code = db.Column(db.String(255), nullable=True)
    starling_webhook_secret = db.Column(db.String(255), nullable=True)

    def requires_authentication(self):
        return not self.starling_authenticated() or not self.ynab_authenticated()

    def starling_authenticated(self):
        return self.starling_auth_code is not None

    def ynab_authenticated(self):
        return self.ynab_auth_code is not None


@event.listens_for(User, 'before_insert')
def receive_before_insert(mapper, connection, target):
    if target.uuid is None:
        target.uuid = str(uuid.uuid4())
