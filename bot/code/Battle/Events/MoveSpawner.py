
from . import Moves


class MoveSpawner:
    """Return move objects to simplify other code
    """
    moves = {
        10: Moves.M010_Scratch,
        33: Moves.M033_Tackle,
        165: Moves.M165_Struggle,
    }

    def __init__(self):
        pass


    @classmethod
    async def get_move(cls, move_id):
        move_id = int(move_id)

        move = cls.moves.get(move_id, lambda *x, **y: None)

        return move
