from ...Pokemon.Enums import EnumMoveCategory as MC

from .EventBase import EventBase



class EventMove(EventBase):


    def __init__(self, battle, user, target=None):
        """Given a Move object, create a new even to handle this attack.
        """
        super().__init__(battle)
        self.user = user
        self.target = target


    async def execute(self, *args, **kwargs):
        """ Implement in other classes. Depending on the event,
        """
        print(MC)


    async def _find_target_poke(self):
        """Attempt to find our target
        """
        for side in self.battle.pokemon_on_field:
            for pokemon in side:
                if pokemon != self.user:
                    return pokemon

        raise RuntimeError("Couldn't find a participant in battle!")
