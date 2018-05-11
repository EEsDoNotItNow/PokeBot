

from ..SQL import SQL
from ..Log import Log


class Type:
    """Handle basic maths of types
    """

    sql = SQL()
    log = Log()


    def __init__(self, type_id):
        self.type_id = type_id
        self.identifier = self.sql.cur.execute("SELECT identifier FROM types WHERE type_id=:type_id", locals()).fetchone()['identifier']


    def __str__(self):
        return f"{self.identifier}"



