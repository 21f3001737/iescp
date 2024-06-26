from werkzeug.exceptions import HTTPException
from flask import make_response

class NotFoundError(HTTPException):
    def __init__(self, status_code, status_message):
        self.response= make_response(json.dumps({'error-message': status_message}), status_code)

class CreationError(HTTPException):
    def __init__(self, status_code, object_type, status_message, error_code):
        self.response = make_response(json.dumps({'for-object': object-type,'error-message': status_message, 'error-code': error_code}), status_code)
