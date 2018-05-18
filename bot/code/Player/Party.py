
from ..Pokemon import Monster



class Party:
    """Manage a players pokemon, their interactions, and other such things
    """

    def __init__(self, trainer_id):
        self.trainer_id = trainer_id


    async def add(self, monster):
        """Add pokemon to the party

        @param monster a Monster object to add to the party
        """
        if type(monster) != Monster:
            raise ValueError


    async def remove(self, target):
        """
        @param target Can be Monster or Int. If Int, remove that slot's monster (zero indexed)

        @return Monster that was removed
        """
        pass
