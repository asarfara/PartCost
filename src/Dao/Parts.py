import logging
import json

from typing import List
from src.Entity.Part import Part
from datetime import date
from sqlite3 import Connection


class Parts:
    def __init__(self, file_name: str, logger: logging, connection: Connection):
        self.file_name = file_name
        self.logger = logger
        self.connection = connection

    def insert_parts(self, parts: List[Part]):
        """Insert collection of parts into the database.

        Args:
            parts (List[Part]): Collection of parts.
        """

        cursor = self.connection.cursor()

        for part in parts:
            self.logger.debug("Inserting into price_parts {0}".format(json.dumps(part.__dict__)))
            cursor.execute('INSERT INTO parts_price (name, price, supplier, type, date) VALUES (?,?,?,?,?)', [part.name, part.price, part.supplier, part.type, date.today()])
            self.connection.commit()

        return None
