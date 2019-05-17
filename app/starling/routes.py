from flask import request, abort, jsonify

from app import db
from app.starling import bp
from app.starling.models import StarlingTransaction
from app.starling.parsers import StarlingWebhookParser
from app.users.models import User


@bp.route('/webhook/<string:uuid>', methods=['POST'])
def webhook(uuid):
    user = User.query.filter_by(uuid=uuid).first()
    if user is None:
        abort(404)

    trans_data = StarlingWebhookParser(request.get_json()).parse()
    trans = StarlingTransaction.query.filter_by(
        transaction_uid=trans_data['transaction_uid']
    ).first()

    status = 200
    if trans is None:
        trans = StarlingTransaction(**trans_data)
        db.session.add(trans)
        status = 201
    else:
        trans.update(trans_data)
        db.session.commit()

    response = jsonify({'success': True})
    response.status_code = status
    return response
