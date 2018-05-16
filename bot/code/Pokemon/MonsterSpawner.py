
import numpy as np

from ..SQL import SQL
from ..Log import Log
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

        # NOTE: This is how monsters must be spawned, as we cannot call async functions in __init__!!!
        poke = Monster(pokemon_id)
        await poke.load()

        poke.xp = np.random.randint(0, 1e6)

        poke.iv_hp = np.random.randint(0, 31)
        poke.iv_attack = np.random.randint(0, 31)
        poke.iv_defense = np.random.randint(0, 31)
        poke.iv_sp_attack = np.random.randint(0, 31)
        poke.iv_sp_defense = np.random.randint(0, 31)
        poke.iv_speed = np.random.randint(0, 31)

        await poke.update_state()

        return poke
