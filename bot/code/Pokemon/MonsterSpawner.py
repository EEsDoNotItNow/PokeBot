

from ..SQL import SQL
from ..Log import Log
from .Pokemon import Pokemon
from .Monster import Monster

class MonsterSpawner:
    """Handle creation of wild spawns, or other random creatures!
    """

    def __init__(self):
        self.sql = SQL()
        self.log = Log()


    async def spawn_random(self):
        """ Pick a poke at random from the dex and spawn it!
        """
        cur = self.sql.cur

        cmd = "SELECT pokemon_id FROM pokedex ORDER BY RANDOM() LIMIT 1"
        pokemon_id = cur.execute(cmd).fetchone()['pokemon_id']

        poke = Monster(pokemon_id)
        await poke.load()

        return poke

