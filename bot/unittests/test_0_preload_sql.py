

import numpy as np
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
        # Placeholder assert to force a setUp and tearDown
        self.assertEqual(1,1)        
