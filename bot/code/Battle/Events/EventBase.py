from ...Log import Log



class EventBase:
    """Define the base event for battle events.
    """


    def __init__(self, battle):

        # Mark when event has started
        self.triggered = False

        # Mark when event has started
        self.completed = False

        # Mark even ready for processing
        self.ready = False

        self.battle = battle

        self.turns = -1

        self.log = Log()


    async def _find_target_poke(self):
        """Attempt to find our target
        """
        for side in self.battle.pokemon_on_field:
            for pokemon in side:
                if pokemon != self.user:
                    return pokemon

        raise RuntimeError("Couldn't find a participant in battle!")


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


    async def on_damage(self, target):
        """Called when a Pokemon takes damage
        """
        pass


    async def on_feint(self, feinter):
        """Called when a Pokemon feints
        """
        pass
