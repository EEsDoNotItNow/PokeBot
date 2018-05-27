
from . import Moves


class MoveSpawner:
    """Return move objects to simplify other code
    """
    moves = {
        33: Moves.M33_Tackle,
        165: Moves.M165_Struggle,
    }

    def __init__(self):
        pass


    @classmethod
    async def get_move(cls, move_id):
        move_id = int(move_id)

        move = cls.moves.get(move_id, lambda: None)

        return move
