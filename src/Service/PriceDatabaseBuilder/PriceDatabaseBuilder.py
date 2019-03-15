import logging

from sqlite3 import Error, Connection


class PriceDatabaseBuilder:
    def __init__(self, file_name: str, logger: logging, connection: Connection):
        self.file_name = file_name
        self.logger = logger
        self.connection = connection

    def create_table(self):
        sql_create_parts_price_table = """ CREATE TABLE IF NOT EXISTS parts_price (
                                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                                               name TEXT NOT NULL,
                                               price REAL NOT NULL,
                                               supplier TEXT NOT NULL,
                                               type TEXT NOT NULL,
                                               date TEXT NOT NULL
                                           ); """
        try:
            self.logger.debug("Creating table parts_price if it doesn't exists")
            cursor = self.connection.cursor()
            cursor.execute(sql_create_parts_price_table)
        except Error as e:
            raise Exception("Exception occurred while trying to create a table: {0}".format(e))
