from flask import render_template
from flask_login import login_required
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
