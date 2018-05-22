
from ..Pokemon import Monster

from ..Singleton import SingletonArgs



class BattleHelper:


    def __init__(self, battle_id, turn):
        self.battle_id = battle_id
        self.turn = turn

        self.participants = []

        self.effects = []

        self.has_run = False

        self._log = []


    ## Add a monster to the planned execution
    # @param monster Monster to be added (order doesn't matter)
    # @param move Move number to execute
    async def register(self, element, mod=None):
        if type(element) == Monster:
            if monster not in [x[0] for x in self.participants]:
                self.participants.append((monster,move))
        else:
            pass


    async def deregister(self, monster):
        self.participants = [x for x in self.participants if x[0] is not mosnter]


    async def get_log(self):
        return self._log


    async def execute(self):
        if self.has_run:
            return
        self.has_run = True


