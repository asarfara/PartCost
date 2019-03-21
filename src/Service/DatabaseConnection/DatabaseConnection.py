import logging
import sqlite3

from sqlite3 import Error, Connection


class DatabaseConnection:
    """
    Create a database connection.
    """

    def __init__(self, file_name: str, logger: logging):
        self.file_name = file_name
        self.logger = logger

    def create_connection(self) -> Connection:
        """
        Create connection with the database.

        Returns:
            Connection: The database connection object.
        """

        try:
            self.logger.debug("Creating connection in {0}".format(self.file_name))
            return sqlite3.connect(self.file_name)
        except Error as e:
            raise Exception("Exception occurred while trying to create a connection: {0}".format(e))
