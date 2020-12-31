class ItemAlreadyStored(Exception):
    pass


class ItemNotStored(Exception):
    pass


class ConnectionError(Exception):
    pass


class TimeoutError(Exception):
    pass


class InternalError(Exception):
    pass


class IntegrityError(Exception):
    pass


class DatabaseError(Exception):
    pass
