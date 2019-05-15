from flask import Blueprint

bp = Blueprint('starling', __name__, template_folder='templates')

from app.starling import routes, models  # noqa