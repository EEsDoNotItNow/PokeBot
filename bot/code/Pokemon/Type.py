

from ..SQL import SQL
from ..Log import Log


class Type:
    """Handle basic maths of types
    """

    sql = SQL()
    log = Log()

    type_efficacy = None

    def __init__(self, type_id):
        self.type_id = type_id
        self.identifier = self.sql.cur.execute("SELECT identifier FROM types WHERE type_id=:type_id", locals()).fetchone()['identifier']

        if not Type.type_efficacy:
            Type.type_efficacy = True
            data = self.sql.cur.execute("SELECT * FROM type_efficacy").fetchall()
            Type.type_efficacy = {}
            for entry in data:
                if entry['damage_type_id'] not in Type.type_efficacy:
                    Type.type_efficacy[entry['damage_type_id']] = {}
                Type.type_efficacy[entry['damage_type_id']][entry['target_type_id']] = entry['damage_factor']


    def __str__(self):
        return f"{self.identifier}"


    def __mul__(self, other):
        damage_factor = Type.type_efficacy[self.type_id][other.type_id]

        return damage_factor/100


