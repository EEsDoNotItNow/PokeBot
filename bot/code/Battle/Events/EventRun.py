import numpy as np

from .EventBase import EventBase



class EventRun(EventBase):
    """Define the base event for battle events.
    """

    def __init__(self, battle, user):
        """Given a Move object, create a new event to handle this attack.
        """
        super().__init__(battle)
        self.user = user


    async def execute(self, *args, **kwargs):
        """ Implement in other classes. Depending on the event,
        """
        self.log.info("Executing")

        # Attempt to run away

        # Formula = ((A *128 / B) + 30 * C) % 256

        A = self.user.speed

        B = (await self._find_target_poke()).speed

        C = self.battle.turn

        F = ((A * 128 / B) + 30 * C)

        if 0 and F > 256 or np.random.randint(256) < F:
            self.battle.active = False
            await self.battle.log_event(f"{self.user.name} ran away!")
            return

        await self.battle.log_event(f"{self.user.name} couldn't get away!")
