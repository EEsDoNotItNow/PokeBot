
import asyncio
import uuid

# from ..Pokemon import Monster

from ..Log import Log
from ..Player import Trainer
from ..Pokemon import Pokemon
from ..Singleton import SingletonArgs

from .Events import EventBase


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

        # Participant location indicates Pokemon location!
        self.pokemon_on_field = [[], []]

        self.events = []

        self.effects = []

        self._log = {}
        self.log = Log()


    async def register(self, participant):
        """Register a participant with the battle
        """
        if participant in self.participants:
            raise ValueError(f"Participant {participant} already in battle!")
        else:
            self.participants.append(participant)

        side_of_field = self.participants.index(participant)
        if isinstance(participant, Trainer):
            poke = await participant.party.get_leader()
            self.pokemon_on_field[side_of_field].append(poke)
        elif isinstance(participant, Pokemon):
            self.pokemon_on_field[side_of_field].append(participant)


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

        self._log[self.turn] = []

        try:
            # Handle any run events
            for event in self.events:
                self.log.info(f"Found event {event}")
                if not isinstance(event, EventBase):
                    self.log.error(f"Found {event} in {self.events}, this should never happen.")
                    continue

                await event.execute()

                # Check all active Pokemon for hp <= 0, mark them as feigned

                # Fight all feigned Pokemon, remove them from the battle field

                # Is the battle over?
                if not self.active:
                    self.log.info("Battle is now completed, ending!")
                    return

        except Exception:
            self.log.exception("Caught while running Battle.execute.")
        finally:
            self.executing = False
            self.turn += 1
            self.log.info(f"Finished on turn {self.turn}")


    async def on_swap(self, swapper):
        """Called when a Pokemon swaps
        """
        pass


    async def on_attack(self, attacker, target):
        """Called when a Pokemon attacks a target
        """
        pass


    async def on_feint(self, attacker, target):
        """Called when a Pokemon feints
        """
        pass
