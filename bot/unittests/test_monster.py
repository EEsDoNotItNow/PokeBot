

import logging
import numpy as np
import sys
import unittest

from ._run import _run

from ..code.Pokemon import Monster
from ..code.SQL import SQL



class test_monster(unittest.TestCase):


    def setUp(self):
        self.sql = SQL("poke.db")

        # We cannot run async calls from here, use _run
        _run(self.sql.on_ready())


    def tearDown(self):
        del self.sql

    def test_create_all_monsters(self):
        for i in range(1, 807 + 1):
            poke = Monster(pokemon_id=i)

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

    def test_safe_and_load_monsters(self):
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

            poke2 = Monster(pokemon_id=i, monster_id=example_id)

            _run(poke2.load())

            self.assertEqual(poke.monster_id, poke2.monster_id)
