from flask import Blueprint

bp = Blueprint('ynab', __name__, template_folder='templates')

from app.ynab import routes, models  # noqa
