import base64
import hashlib
import json

from flask import request
from dateutil import parser

from app import db
from app.helpers import json_response
from app.starling import bp
from app.starling.models import StarlingTransaction
from app.users.models import User


@bp.route('/webhook/<string:uuid>', methods=['POST'])
def webhook(uuid):
    user = User.query.filter_by(uuid=uuid).first()
    if user is None:
        return json_response(404, {
            'success': False,
            'message': 'User does not exist'
        })

    body = request.get_data(as_text=True)
    signature = str(request.headers.get('X-Hook-Signature'))
    hash = hashlib.sha512(str(user.starling_webhook_secret + body).encode('utf-8'))
    encoded = base64.b64encode(hash.digest()).decode("utf-8")

    print('--- THEIR SIGNATURE ---')
    print(signature)
    print('--- OUR SIGNATURE ---')
    print(encoded)
    print('---------------')

    # TODO: test this with actual request
    if False and signature != encoded:
        return json_response(403, {
            'success': False,
            'message': 'Invalid signature'
        })

    json_data = json.loads(body)
    trans_data = {
        'user_id': user.id,
        'transaction_uid': json_data['content']['transactionUid'],
        'amount': json_data['content']['amount'],
        'transaction_type': json_data['content']['type'],
        'payee': json_data['content']['counterParty'],
        'transaction_date': parser.parse(json_data['timestamp']),
    }
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
        db.session.merge(trans)

    db.session.commit()

    return json_response(status, {'success': True})
