from flask_login import current_user

from app.ynab import bp
from app.ynab.api import YNABApi


@bp.route('/test-create-trans', methods=['GET'])
def test_create_trans():
    y = YNABApi(current_user)
    raise Exception(y.get_accounts())
    pass