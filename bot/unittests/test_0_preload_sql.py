
import unittest

from .helpers import _run

from ..code.SQL import SQL



class test_0_preload_sql(unittest.TestCase):


    def setUp(self):
        self.sql = SQL("poke.db")

        # We cannot run async calls from here, use _run
        _run(self.sql.on_ready())


    def tearDown(self):
        del self.sql

    def test_create_all_monsters(self):
        # Placeholder assert to force a setUp and tearDown
        self.assertEqual(1, 1)
