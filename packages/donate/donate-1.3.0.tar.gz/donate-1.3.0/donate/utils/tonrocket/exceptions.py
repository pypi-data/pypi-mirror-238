class Unauthorized(Exception):
    def __init__(self, message="[Error]: Unauthorized"):
        self.message = message
        super().__init__(self.message)

class ExpiredIn(Exception):
    def __init__(self, message="[Error]: ExpiredIn must be at least 60 seconds!"):
        self.message = message
        super().__init__(self.message)

class BadRequest(Exception):
    def __init__(self, message):
        self.message = f'[Error: {message.get("property")}] {message.get("error")}'
        super().__init__(self.message)

class Forbidden(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class NotFound(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class InternalServerError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class DictError(Exception):
    def __init__(self):
        self.message = "dict is require"
        super().__init__()

class UnknownError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def check_exceptions(code=0, **kwargs):
    if int(code) == 401:
        raise Unauthorized
    elif int(code) == 60:
        raise ExpiredIn
    elif int(code) == 400:
        raise BadRequest(message=kwargs.get("errors")[0])
    elif int(code) == 403:
        raise Forbidden(message=kwargs.get("message"))
    elif int(code) == 404:
        raise NotFound(message=kwargs.get("message"))
    elif int(code) == 500:
        raise InternalServerError(message=kwargs.get("message"))
    else:
        raise UnknownError(message=kwargs)

