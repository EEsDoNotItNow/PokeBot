
from ..Pokemon import Monster

from ..Singleton import SingletonArgs



class BattleHelper(metaclass=SingletonArgs):


    def __init__(self, battle_id, encounter=False, trainer=False, players=False):
        self.battle_id = battle_id
        self.turn = 0

        self.participants = []

        self.effects = []

        self._log = {}


    async def register(self, trainer):
        """Register a trainer with the battle
        """
        pass


    async def deregister(self, monster):
        self.participants = [x for x in self.participants if x[0] is not mosnter]


    async def get_log(self, full=False):
        return self._log


    async def mark_ready(self, trainer):
        """
        Mark yourself as read for the turn to begin. 
        """

    async def execute(self):
        """
        Simulate the turn
        """
        if self.has_run:
            return
        self.has_run = True


