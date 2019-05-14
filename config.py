import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LOG_FILE = '/var/log/ftrack/ftrack.log'

    # Email
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 25))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['nick.ir.ross@gmail.com']

    # YNAB
    YNAB_CLIENT_ID = os.environ.get('YNAB_CLIENT_ID')
    YNAB_CLIENT_SECRET = os.environ.get('YNAB_CLIENT_SECRET')

    # Starling - TODO: Not implemented yet
    STARLING_CLIENT_ID = os.environ.get('STARLING_CLIENT_ID')
    STARLING_CLIENT_SECRET = os.environ.get('STARLING_CLIENT_SECRET')
