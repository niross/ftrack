from functools import wraps

from flask import current_app, flash, redirect, url_for
from flask_login import current_user


def requires_external_auth(func):
    """
    Decorator that redirects the user to the starling/ynab auth page
    if they have not authorised access for us yet.
    :param func:
    :return:
    """

    @wraps(func)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        if current_user.requires_authentication():
            flash(
                'Please authenticate with both Starling & YNAB to enable financial tracking',
                category='danger'
            )
            return redirect(url_for('main.platform_auth'))
        return func(*args, **kwargs)
    return decorated
