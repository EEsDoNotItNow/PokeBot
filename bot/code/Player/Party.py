
from ..Pokemon import Monster



class Party:
    """Manage a players pokemon, their interactions, and other such things
    """


    def __init__(self, trainer_id):
        self.trainer_id = trainer_id
        self.monsters = [None, None, None, None, None, None]


    def __len__(self):
        return len(self._monsters_not_none)


    def __iter__(self):
        for poke in self._monsters_not_none:
            yield poke


    def __contains__(self, item):
        for poke in self.monsters:
            if item == poke:
                return True
        return False


    @property
    def _monsters_not_none(self):
        return [x for x in self.monster if x is not None]


    async def load(self):
        """Load pokes from DB
        """
        pass


    async def save(self, monster):
        """Saves pokes to DB
        """
        pass


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
