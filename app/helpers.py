from flask import jsonify


def mask_string(string, visible=4):
    size = len(string) - visible
    return string[0:visible + 1] + ('*' * size)


def json_response(status_code, data=None):
    response = jsonify(data or {})
    response.status_code = status_code
    return response
