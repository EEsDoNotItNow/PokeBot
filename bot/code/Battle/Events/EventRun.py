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
        self.battle.active = False
        await self.battle.log_event(f"{self.user} ran away!")
