from ...Log import Log



class EventBase:
    """Define the base event for battle events.
    """


    def __init__(self, battle):

        # Mark when event has been processed.
        self.triggered = False

        # Mark even ready for processing
        self.ready = False

        self.battle = battle

        #
        self.turns = -1
        self.log = Log()
        pass


    async def setup(self):
        """This event is ready for use, mark it as such
        """
        self.ready = True


    async def execute(self, *args, **kwargs):
        """ Implement in other classes. Depending on the event,
        """
        raise NotImplementedError()


    async def tear_down(self):
        """This event has been run, prevent another run before a setup
        """
        if self.triggered or not self.ready:
            raise RuntimeError(f"{self} was not ready! Triggered state: {self.triggered} Ready state: {self.ready}")
        self.triggered = True


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
