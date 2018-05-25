
import uuid

# from ..Pokemon import Monster

from ..Singleton import SingletonArgs



class Battle(metaclass=SingletonArgs):


    def __init__(self, battle_id=None, encounter=False, trainer=False, players=False):

        if battle_id is None:
            self.battle_id = str(uuid.uuid4())
        else:
            self.battle_id = battle_id

        self.active = True

        self.turn = 0

        self.participants = []

        self.effects = []

        self._log = {}


    async def register(self, participant):
        """Register a participant with the battle
        """
        if participant in self.participants:
            raise ValueError(f"Participant {participant} already in battle!")
        self.participants.append(participant)


    async def deregister(self, participant):
        self.participants = [x for x in self.participants if x[0] is not participant]


    async def get_log(self, full=False):
        return self._log


    async def log_event(self, message):
        if self.turn not in self._log:
            self._log[self.turn] = []
        self._log[self.turn].append(message)


    async def mark_ready(self, trainer):
        """
        Mark yourself as read for the turn to begin.
        """
        pass


    async def execute(self):
        """
        Simulate the turn
        """
        if self.has_run:
            return
        self.has_run = True
