
from ..Client import Client
from ..Log import Log
from ..SQL import SQL

from .Pokemon import Pokemon

class Monster(Pokemon):


    def __init__(self, pokemon_id, monster_id=None):
        """Create a new Monster (an acutal pokemon in the sim)

        @param pokemon_id Id from the pokedex table, stats are based off this value
        @param monster_id if given, load all other values from the DB
        """
        self.log = Log()
        self.sql = SQL()

        # Init our superclass
        super().__init__(pokemon_id)

        self.monster_id = monster_id


    async def load(self):
        await super().load()

        if self.monster_id:
            # TODO: Load from SQL
            raise NotImplementedError()

        # TODO: We also need to load from the SQL 
