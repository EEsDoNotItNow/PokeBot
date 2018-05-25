
import asyncio
import uuid

# from ..Pokemon import Monster

from ..Singleton import SingletonArgs
from ..Log import Log

from .EventRun import EventRun


class Battle(metaclass=SingletonArgs):


    def __init__(self, battle_id=None, encounter=False, trainer=False, players=False):

        if battle_id is None:
            self.battle_id = str(uuid.uuid4())
        else:
            self.battle_id = battle_id

        self.active = True

        # Marked true while someone is executing the turn
        self.executing = False

        self.turn = 0

        self.participants = []

        self.events = []

        self.effects = []

        self._log = {}
        self.log = Log()


    async def register(self, participant):
        """Register a participant with the battle
        """
        if participant in self.participants:
            raise ValueError(f"Participant {participant} already in battle!")
        self.participants.append(participant)


    async def deregister(self, participant):
        self.participants = [x for x in self.participants if x[0] is not participant]


    async def register_event(self, event):
        """Register a event with the battle
        """
        if event in self.events:
            raise ValueError(f"Event {event} already in battle!")
        self.events.append(event)


    async def deregister_event(self, event):
        self.events = [x for x in self.events if x[0] is not event]


    async def get_log(self, turn):
        return self._log[turn]


    async def log_event(self, message):
        self.log.info(f"Registered message '{message}' to turn {self.turn}")
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
        self.log.info(f"Called on turn {self.turn}")
        if self.executing:
            while self.executing:
                await asyncio.sleep(1)
            return

        self.executing = True

        try:
            # Handle any run events
            for event in self.events:
                self.log.info(f"Found event {event}")
                if type(event) is not EventRun:
                    continue

                await event.execute()

                # Is the battle over?
                if not self.active:
                    return

        except Exception:
            self.log.exception("Caught while running Battle.execute.")
        finally:

            self.executing = False
            self.turn += 1
            self.log.info(f"Finished on turn {self.turn}")
