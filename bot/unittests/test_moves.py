
import unittest

from .helpers import _run

from ..code.SQL import SQL
from ..code.Pokemon import Move



class test_moves(unittest.TestCase):


    def setUp(self):
        self.sql = SQL("poke.db")

        # We cannot run async calls from here, use _run
        _run(self.sql.on_ready())


    def test_import_all_moves(self):
        for i in range(1, 728 + 1):
            move = Move(move_id=i)

            # We cannot run async calls from here, use _run
            _run(move.load())
            move.__str__()
            move.__repr__()
            _run(move.em())
            self.assertEqual(move.move_id, str(i))
