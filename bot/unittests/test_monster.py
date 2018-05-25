

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
        """Test spawn of every Pokemon
        """
        for i in range(1, 807 + 1):
            with self.subTest(pokemon_id=i):
                poke = Monster(pokemon_id=i)
                _run(poke.spawn(fast=True))
                # We cannot run async calls from here, use _run
                self.assertEqual(str(poke.pokemon_id), str(i))


    def test_01_create_all_monsters_some_levels(self):
        """Test every Pokemon with various key levels
        """
        for i in range(1, 807 + 1):
            for level in [1, 2, 10, 20, 30, 40, 50, 60, 70, 80, 90, 99, 100]:
                with self.subTest(pokemon_id=i, level=level):
                    poke = Monster(pokemon_id=i)
                    _run(poke.spawn(level, fast=True))
                    self.assertEqual(level, poke.level)


    def test_03_save_and_load_monsters(self):
        """Create, save, then reload every Pokemon from the DB
        """
        for i in range(1, 807 + 1):
            poke = Monster(pokemon_id=i)
            _run(poke.spawn(fast=True))
            _run(poke.save())
            example_id = poke.monster_id
            poke2 = Monster(monster_id=example_id, pokemon_id=i)
            _run(poke2.load())
            self.assertEqual(poke.monster_id, poke2.monster_id)
