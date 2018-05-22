

import numpy as np
import unittest

from .helpers import _run

from ..code.Pokemon import Monster
from ..code.SQL import SQL



class test_monster(unittest.TestCase):


    def setUp(self):
        self.sql = SQL("poke.db")

        # We cannot run async calls from here, use _run
        _run(self.sql.on_ready())


    def tearDown(self):
        del self.sql


    def test_00_create_all_monsters(self):
        for i in range(1, 807 + 1):
            with self.subTest(pokemon_id=i):
                poke = Monster(pokemon_id=i)
                print(poke)

                _run(poke.load())

                poke.xp = np.random.randint(0, 1e6)

                poke.iv_hp = np.random.randint(0, 31)
                poke.iv_attack = np.random.randint(0, 31)
                poke.iv_defense = np.random.randint(0, 31)
                poke.iv_sp_attack = np.random.randint(0, 31)
                poke.iv_sp_defense = np.random.randint(0, 31)
                poke.iv_speed = np.random.randint(0, 31)

                _run(poke.update_state())

                # We cannot run async calls from here, use _run
                self.assertEqual(str(poke.pokemon_id), str(i))


    def test_01_create_all_monsters_all_levels(self):
        for i in range(1, 807 + 1):
            for level in range(1, 101):
                with self.subTest(pokemon_id=i, level=level):
                    poke = Monster(pokemon_id=i)
                    _run(poke.load())

                    growth_rate_id = poke.growth_rate_id

                    cmd = """
                        SELECT experience
                        FROM experience_lookup
                        WHERE
                            growth_rate_id=:growth_rate_id
                            AND level=:level
                    """
                    poke.xp = self.sql.cur.execute(cmd, locals()).fetchone()['experience']

                    poke.iv_hp = np.random.randint(0, 31)
                    poke.iv_attack = np.random.randint(0, 31)
                    poke.iv_defense = np.random.randint(0, 31)
                    poke.iv_sp_attack = np.random.randint(0, 31)
                    poke.iv_sp_defense = np.random.randint(0, 31)
                    poke.iv_speed = np.random.randint(0, 31)

                    _run(poke.update_state())


                    self.assertEqual(level, poke.level)


    def test_03_save_and_load_monsters(self):
        for i in range(1, 807 + 1):
            poke = Monster(pokemon_id=i)

            _run(poke.load())

            # Invent some random data to save
            poke.xp = np.random.randint(0, 1e6)
            poke.iv_hp = np.random.randint(0, 31)
            poke.iv_attack = np.random.randint(0, 31)
            poke.iv_defense = np.random.randint(0, 31)
            poke.iv_sp_attack = np.random.randint(0, 31)
            poke.iv_sp_defense = np.random.randint(0, 31)
            poke.iv_speed = np.random.randint(0, 31)
            _run(poke.update_state())

            _run(poke.save())

            example_id = poke.monster_id

            poke2 = Monster(monster_id=example_id, pokemon_id=i)

            _run(poke2.load())

            self.assertEqual(poke.monster_id, poke2.monster_id)
