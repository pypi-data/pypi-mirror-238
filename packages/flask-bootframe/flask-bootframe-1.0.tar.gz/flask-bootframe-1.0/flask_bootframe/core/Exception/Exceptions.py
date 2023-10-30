from werkzeug.exceptions import HTTPException


class BootException(HTTPException):
    code = 500
    description = 'Server Error'

    def __init__(self, msg: str):
        self.description = msg
