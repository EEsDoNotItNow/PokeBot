from ..EventMove import EventMove


class M165_Struggle(EventMove):


    def __init__(self, battle, user, target=None):
        super().__init__(battle, user, target)


    async def execute(self):
        """ Implement in other classes. Depending on the event,
        """
        raise NotImplementedError()
