class RequestException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class MissingAttributeException(Exception):
    def __init__(self, message: str, attribute: str):
        super().__init__(message, attribute)
