from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app import db
from app.main import bp
from app.main.decorators import requires_external_auth
from app.users.forms import StarlingAuthForm


@bp.route('/')
@login_required
@requires_external_auth
def home():
    return render_template(
        'main/home.html',
        title='Home'
    )


@bp.route('/platform/auth', methods=['GET', 'POST'])
@login_required
def platform_auth():
    form = StarlingAuthForm()
    show_starling_modal = False
    if form.validate_on_submit():
        current_user.starling_auth_code = form.starling_auth_code.data
        current_user.starling_webhook_secret = form.starling_webhook_secret.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('main.platform_auth'))
    elif request.method == 'GET':
        form.starling_auth_code.data = current_user.starling_auth_code
        form.starling_webhook_secret.data = current_user.starling_webhook_secret
    else:
        show_starling_modal = True

    return render_template(
        'main/platform_auth.html',
        starling_form=form,
        show_starling_modal=show_starling_modal
    )


@bp.route('/platform/auth/ynab/unlink')
@login_required
def ynab_unlink():
    current_user.ynab_auth_code = None
    db.session.commit()
    flash('YNAB account successfully unlinked')
    return redirect(url_for('main.platform_auth'))


@bp.route('/platform/auth/starling/unlink')
@login_required
def starling_unlink():
    current_user.starling_auth_code = None
    db.session.commit()
    flash('Starling account successfully unlinked')
    return redirect(url_for('main.platform_auth'))
