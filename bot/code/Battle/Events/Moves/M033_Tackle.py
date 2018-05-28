import numpy as np

from ....Pokemon import Move
from ..EventMove import EventMove



class M033_Tackle(EventMove):


    def __init__(self, battle, user, target=None):
        super().__init__(battle, user, target)

        self.move = Move(33)


    async def execute(self):
        """ Implement in other classes. Depending on the event,
        """
        target = await self._find_target_poke()
        if not self.move.move_loaded:
            await self.move.load()

        self.log.info(f"Targeting {target} ({type(target)}) with a tackle!")

        A = self.user.attack

        D = target.defense

        level = self.user.level

        power = self.move.power

        self.log.info(locals())

        base_damage = (((2 * level) / 5 + 2) * (power * A / D)) / 50 + 2

        modifier = np.random.uniform(0.85, 1.0)

        damage = int(base_damage * modifier)

        await target.damage(damage)

        await self.battle.log_event(f"{self.user.name} hit {target.name} for {damage}!")

        self.triggered = True
        self.completed = True
