from ..EventMove import EventMove


class M033_Tackle(EventMove):


    def __init__(self, battle, user, target=None):
        super().__init__(battle, user, target)


    async def execute(self):
        """ Implement in other classes. Depending on the event,
        """
        target = await self._find_target_poke()

        self.log.info(f"Targeting {target} ({type(target)}) with a tackle!")
