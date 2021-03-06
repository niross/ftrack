from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app import db
from app.main import bp
from app.main.decorators import requires_external_auth
from app.users.forms import PlatformAuthForm
from app.ynab.api import YNABApi


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
    form = PlatformAuthForm()
    if current_user.ynab_auth_code is not None:
        ynab_api = YNABApi(current_user)

        for account in ynab_api.get_accounts()['data']['accounts']:
            form.ynab_account_id.choices.append(
                (account['id'], account['name'])
            )

        for cat_group in ynab_api.get_categories()['data']['category_groups']:
            for category in cat_group['categories']:
                form.ynab_category_id.choices.append(
                    (category['id'], category['name'])
                )

    if form.validate_on_submit():
        current_user.starling_auth_code = form.starling_auth_code.data
        current_user.starling_webhook_secret = form.starling_webhook_secret.data
        current_user.ynab_auth_code = form.ynab_auth_code.data
        current_user.ynab_account_id = form.ynab_account_id.data
        current_user.ynab_category_id = form.ynab_category_id.data
        db.session.commit()
        flash('Your changes have been saved', category='success')
        return redirect(url_for('main.platform_auth'))
    elif request.method == 'GET':
        form.starling_auth_code.data = current_user.starling_auth_code
        form.starling_webhook_secret.data = current_user.starling_webhook_secret
        form.ynab_auth_code.data = current_user.ynab_auth_code
        form.ynab_account_id.data = current_user.ynab_account_id
        form.ynab_category_id.data = current_user.ynab_category_id
    else:
        flash('Please fix any errors on the form', category='danger')

    return render_template(
        'main/platform_auth.html',
        form=form
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
