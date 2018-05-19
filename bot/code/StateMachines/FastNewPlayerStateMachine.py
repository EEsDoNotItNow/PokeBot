
import numpy as np

from ..Client import Client
from ..Log import Log
from ..Player import League
from ..Pokemon import MonsterSpawner
from ..SQL import SQL

from .BaseStateMachine import BaseStateMachine



class FastNewPlayerStateMachine(BaseStateMachine):
    """"Handle a new players creation process
    """

    def __init__(self, trainer):
        super().__init__()

        # Need to type check this bad boy
        self.trainer = trainer

        self.client = Client()
        self.sql = SQL()
        self.log = Log()


    async def run(self):
        """Run through the player creation process.
        """
        self.started = True
        self.log.info(f"{self.trainer.trainer_id} Begin our run of NewPlayerStateMachine")
        try:
            await self._run()
        except Exception:
            self.log.exception(f"{self.trainer.trainer_id} Something went wrong...")
            await League().deregister(self.trainer.user_id, self.trainer.server_id)
        await self.trainer.save()
        self.log.exception(f"{self.trainer.trainer_id} Saved status and exited NewPlayerStateMachine")

    async def _run(self):

        self.log.info(f"{self.trainer.trainer_id} Creating a new player.")

        user = await self.client.get_user_info(self.trainer.user_id)
        await self.client.start_private_message(user)

        for channel in self.client.private_channels:
            if channel.user == user:
                break

        msg = "DEBUG: Fast Trainer Creation Engaged"
        await self.client.send_message(channel, msg)

        poke1 = await MonsterSpawner().spawn_at_level(1, 5)
        poke2 = await MonsterSpawner().spawn_at_level(4, 5)
        poke3 = await MonsterSpawner().spawn_at_level(7, 5)

        poke_list = [poke1, poke2, poke3]

        prompt_list = [x.identifier for x in poke_list]

        selection = np.random.randint(0, 3)

        self.log.info(f"{self.trainer.trainer_id} User selected {prompt_list[selection]}.")

        await self.trainer.party.add(poke_list[selection])

        msg = "DEBUG: Fast Trainer Creation Completed"
        await self.client.send_message(channel, msg)

        # We are done, die!
        self.alive = False
