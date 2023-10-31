from flask import jsonify


def handle_exception(error):
    response = jsonify(
        {
            'code': error.code,
            'message': error.description
        }
    )
    response.status_code = error.code
    return response
