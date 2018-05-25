
import unittest

from .helpers import _run

from ..code.SQL import SQL
from ..code.Pokemon import MoveSlot


class test_move_slots(unittest.TestCase):


    def setUp(self):
        self.sql = SQL("poke.db")

        # We cannot run async calls from here, use _run
        _run(self.sql.on_ready())


    def test_import_all_move_slots(self):
        """Load up every Move in the DB
        """
        for i in range(1, 728 + 1):
            move_slot = MoveSlot(move_id=i)

            # We cannot run async calls from here, use _run
            _run(move_slot.load())
            move_slot.__str__()
            move_slot.__repr__()
            _run(move_slot.em())
            self.assertEqual(move_slot.move_id, str(i))
