import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_babel import Babel
from flask_mail import Mail
from flask_migrate import Migrate
from flask_scss import Scss
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
bootstrap = Bootstrap()
security = Security()
babel = Babel()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    bootstrap.init_app(app)
    babel.init_app(app)
    Scss(app, asset_dir='app/static/sass', static_dir='app/static/css/compiled')

    from app.main import bp as main_bp  # noqa
    app.register_blueprint(main_bp)

    from app.users import user_datastore, bp as users_bp  # noqa
    app.register_blueprint(users_bp)
    security.init_app(app, user_datastore)

    from app.ynab import bp as ynab_bp
    app.register_blueprint(ynab_bp, url_prefix="/platform/ynab")

    from app.starling import bp as starling_bp
    app.register_blueprint(starling_bp, url_prefix="/platform/starling")

    if not app.debug and not app.testing:
        fh = RotatingFileHandler(config_class.LOG_FILE, maxBytes=10240, backupCount=10)
        fh.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        fh.setLevel(logging.INFO)
        app.logger.addHandler(fh)
        app.logger.setLevel(logging.INFO)
        app.logger.info('FTrack starting')

    return app


