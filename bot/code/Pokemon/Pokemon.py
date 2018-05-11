
from ..SQL import SQL
from ..Log import Log

from .Type import Type

class Pokemon:


    sql = SQL()
    log = Log()


    def __init__(self, _id):

        self.id = int(_id)
        self.identifier = "NOT YET LOADED"
        self.type1 = None
        self.type2 = None


    def __repr__(self):
        return f"Pokemon({self.id})"


    def __str__(self):
        if self.type2:
            type2 = f"/{self.type2}"
        else:
            type2 = ""
        return f"<Pokemon: {self.identifier.title()} ({self.type1}{type2})>"


    async def load(self):
        # Define locals for use in SQL
        pokemon_id = self.id
        cmd = "SELECT * FROM pokedex WHERE pokemon_id=:pokemon_id"
        cur = self.sql.cur
        data = cur.execute(cmd, locals()).fetchone()
        self.log.debug(f"Loaded data: {data}")

        self.identifier = data['identifier']

        self.base_attack = data['base_attack']
        self.base_defense = data['base_defense']
        self.base_hp = data['base_hp']
        self.base_sp_attack = data['base_sp_attack']
        self.base_sp_defense = data['base_sp_defense']
        self.base_speed = data['base_speed']
        self.base_xp = data['base_xp']
        self.effort_attack = data['effort_attack']
        self.effort_defense = data['effort_defense']
        self.effort_hp = data['effort_hp']
        self.effort_sp_attack = data['effort_sp_attack']
        self.effort_sp_defense = data['effort_sp_defense']
        self.effort_speed = data['effort_speed']

        self.abilities = data['abilities']
        self.catch_rate = data['catch_rate']
        self.gender_ratio = data['gender_ratio']
        self.hatch_time = data['hatch_time']
        self.height = data['height']
        self.hidden_abilities = data['hidden_abilities']
        self.type1 = data['type1']
        self.type2 = data['type2']
        self.weight = data['weight']

        self.type1 = Type(self.type1)
        if self.type2:
            self.type2 = Type(self.type2)

