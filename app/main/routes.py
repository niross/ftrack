from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db
from app.main import bp
from app.main.decorators import requires_external_auth


@bp.route('/')
@login_required
@requires_external_auth
def home():
    return render_template(
        'main/home.html',
        title='Home'
    )


@bp.route('/platform/auth')
@login_required
def platform_auth():
    return render_template(
        'main/platform_auth.html'
    )


@bp.route('/platform/auth/ynab/unlink')
@login_required
def ynab_unlink():
    current_user.ynab_auth_code = None
    db.session.commit()
    flash('YNAB account sunccessfully unlinked')
    return redirect(url_for('main.platform_auth'))
