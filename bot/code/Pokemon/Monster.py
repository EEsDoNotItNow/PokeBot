
from ..Log import Log
from ..SQL import SQL

from .Pokemon import Pokemon

class Monster(Pokemon):

    log = Log()
    sql = SQL()

    def __init__(self, pokemon_id, monster_id=None):
        """Create a new Monster (an acutal pokemon in the sim)

        @param pokemon_id Id from the pokedex table, stats are based off this value
        @param monster_id if given, load all other values from the DB
        """

        # Init our superclass
        super().__init__(pokemon_id)

        self.hp = self.base_hp
        self.xp = 0

        if monster_id:
            # TODO: Load from SQL
            raise NotImplementedError()
