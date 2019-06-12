from flask import jsonify
from flask_login import current_user

from app.ynab import bp
from app.ynab.api import YNABApi


@bp.route('/test-create-trans', methods=['GET'])
def test_create_trans():
    y = YNABApi(current_user)
    # return jsonify(y.get_payees())
    return jsonify(y.create_transaction(11.23, 'TEST TEST'))
    resp = y.create_transaction({})
    return jsonify(resp)
