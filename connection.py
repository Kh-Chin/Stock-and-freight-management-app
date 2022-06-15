import pyodbc
import config


class Connection:
    """
    This class is used with the Python "with" statement to build a connection to the
    database based on the configuration in the config.py file.
    """

    def __init__(self):
        self.config = config.connection_string

    def __enter__(self):
        # Connect database
        self.connection = pyodbc.connect(self.config)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exception_type, exception_value, traceback):
        self.connection.commit()
        self.connection.close()
