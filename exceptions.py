"""File which has the exceptions for the pyp_database."""

class DataBaseNotFoundError(Exception):
    pass

class TableNotFoundError(Exception):
    pass

class TableAlreadyExistsError(Exception):
    pass

class DatabaseAlreadyExistsError(Exception):
    pass

class ColumnNotFoundError(Exception):
    pass