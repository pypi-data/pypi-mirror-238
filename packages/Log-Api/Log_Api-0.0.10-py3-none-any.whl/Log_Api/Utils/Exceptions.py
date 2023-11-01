class UserException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class RejectionException(Exception):
    def __init__(self, code: str, data=None):
        self.code = code
        self.data = data
        super().__init__(self.code)