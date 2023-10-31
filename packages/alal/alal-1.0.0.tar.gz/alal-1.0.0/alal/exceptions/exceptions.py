class AlalUnauthorized(Exception):

    def __init__(self, *args):
        self.message = args[0]
        self.code = 401

    @property
    def response(self):
        return {"status": "Unauthorized", "name": "AlalUnauthorized", "code": self.code, "message": self.message}


class AlalBadRequest(Exception):

    def __init__(self, *args):
        self.message = args[0]
        self.code = 400

    @property
    def response(self):
        return {"status": "Unauthorized", "name": "AlalBadRequest", "code": self.code, "message": self.message}


class AlalServerErrors(Exception):
    def __init__(self, *args):
        self.message = args[0]
        self.code = 500

    @property
    def response(self):
        return {"status": "error", "name": "AlalServerErrors", "code": self.code, "message": self.message}


class AlalNotFound(Exception):
    def __init__(self, *args):
        self.message = args[0]
        self.code = 404

    @property
    def response(self):
        return {"status": "error", "name": "AlalNotFound", "code": self.code, "message": self.message}
