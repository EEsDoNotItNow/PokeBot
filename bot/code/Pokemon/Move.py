
import uuid

from ..Log import Log
from ..SQL import SQL


class Move:

    def __init__(self, move_id):
        self.move_id = move_id


class MoveSlot:

    def __init__(self, move_id, move_uuid=None):
        self.move_id = move_id
        self.move_uuid = move_uuid

