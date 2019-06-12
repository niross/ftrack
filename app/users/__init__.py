from flask import Blueprint
from flask_security import SQLAlchemyUserDatastore

from app import db
from app.users.models import User, Role

bp = Blueprint('users', __name__, template_folder='templates')

user_datastore = SQLAlchemyUserDatastore(db, User, Role)


# Create a user to test with
@bp.before_app_first_request
def create_user():
    db.create_all()
    if User.query.filter_by(email='test.user@example.com').count() == 0:
        user_datastore.create_user(email='test.user@example.com', password='password')
        db.session.commit()
