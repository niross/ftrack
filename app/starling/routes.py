from flask import request

from app.starling import bp


@bp.route('/webhook', methods=['GET', 'POST'])
def webhook():
    req = request.get_json()
    raise Exception(req)
