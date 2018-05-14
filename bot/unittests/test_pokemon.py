
import unittest
import logging
import sys
import os

from ._run import _run

from ..code.SQL import SQL
from ..code.Pokemon import Pokemon

class Basic(unittest.TestCase):


    def setUp(self):
        logging.disable(sys.maxsize)
        self.sql = SQL("poke.db")

        # We cannot run async calls from here, use _run
        _run(self.sql.on_ready())


    def test_import_all_pokemon(self):
        for i in range(1,807+1):
            poke = Pokemon(pokemon_id = i)

            # We cannot run async calls from here, use _run
            _run(poke.load())
            poke.__str__()
            poke.__repr__()
            _run(poke.em())
            self.assertEqual(str(poke.pokemon_id),str(i))

