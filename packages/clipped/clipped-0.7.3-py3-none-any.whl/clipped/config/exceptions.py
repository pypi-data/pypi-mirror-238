from click import ClickException


class ClippedException(ClickException):
    def __init__(self, message=None):
        super().__init__(message)

    def __repr__(self):
        return self.message


class SchemaError(ClippedException):
    pass
