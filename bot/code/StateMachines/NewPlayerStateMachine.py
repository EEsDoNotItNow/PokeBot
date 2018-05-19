
import asyncio

from ..Client import Client
from ..Log import Log
from ..Player import League
from ..Pokemon import MonsterSpawner
from ..SQL import SQL

from .BaseStateMachine import BaseStateMachine



class NewPlayerStateMachine(BaseStateMachine):
    """"Handle a new players creation process
    """

    def __init__(self, trainer):
        super().__init__()

        # Need to type check this bad boy
        self.trainer = trainer

        self.client = Client()
        self.sql = SQL()
        self.log = Log()

        self.alive = True


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
            self.alive = False
            
        await self.trainer.save()
        self.log.exception(f"{self.trainer.trainer_id} Saved status and exited NewPlayerStateMachine")

    async def _run(self):

        self.log.info(f"{self.trainer.trainer_id} Creating a new player.")

        user = await self.client.get_user_info(self.trainer.user_id)
        await self.client.start_private_message(user)

        for channel in self.client.private_channels:
            if channel.user == user:
                break

        msg = "`Professor Ironwood`: Hello, and welcome to the Pokemon League!"
        await self.client.send_message(channel, msg)

        prompt = f"Are you ready to begin?"
        response = await self.client.confirm_prompt(channel, prompt, user=user, timeout=60 * 5, clean_up=False)
        if response is not True:
            await self.client.send_typing(channel)
            await asyncio.sleep(4)
            msg = "`Professor Ironwood`: Okay, if you change you mind, you can try to `>register` again!"
            await self.client.send_message(channel, msg)
            raise ValueError("User didn't answer that they were ready to go, abort!")

        await asyncio.sleep(1.5)
        await self.client.send_typing(channel)
        await asyncio.sleep(4)
        msg = "`Professor Ironwood`: You are in for such a huge adventure!"
        await self.client.send_message(channel, msg)

        await asyncio.sleep(1.5)
        await self.client.send_typing(channel)
        await asyncio.sleep(4)
        msg = "`Professor Ironwood`: Before we begin..."
        await self.client.send_message(channel, msg)


        self.log.info(f"{self.trainer.trainer_id} Prompting for a user name.")
        while 1:
            name = await self.client.text_prompt(channel, "What is your name?", user=user)
            self.log.info(f"{self.trainer.trainer_id} Got response of name='{name}'")

            prompt = f"You name is '{name}', is that right?"
            response = await self.client.confirm_prompt(channel, prompt, user=user, timeout=30, clean_up=False)

            if response:
                break
            self.log.info(f"{self.trainer.trainer_id} User rejected with {response}")

        self.trainer.nickname = name
        self.log.info(f"{self.trainer.trainer_id} User selected name of {name}")

        await asyncio.sleep(1.5)
        await self.client.send_typing(channel)
        await asyncio.sleep(5)
        msg = f"`Professor Ironwood`: Okay {name}, let's get you started!"
        await self.client.send_message(channel, msg)

        await asyncio.sleep(1.5)
        await self.client.send_typing(channel)
        await asyncio.sleep(5)
        msg = "`Professor Ironwood`: Where did I keep those things?"
        await self.client.send_message(channel, msg)

        await asyncio.sleep(1.5)
        await self.client.send_typing(channel)
        await asyncio.sleep(2)
        msg = "`Professor Ironwood`: Up here?"
        await self.client.send_message(channel, msg)

        await asyncio.sleep(1.5)
        await self.client.send_typing(channel)
        await asyncio.sleep(7)
        msg = "`Professor Ironwood`: Nope!"
        await self.client.send_message(channel, msg)

        await asyncio.sleep(1.5)
        await self.client.send_typing(channel)
        await asyncio.sleep(2)
        msg = "`Professor Ironwood`: *Looks at the table*"
        await self.client.send_message(channel, msg)

        await asyncio.sleep(1.5)
        await self.client.send_typing(channel)
        await asyncio.sleep(2)
        msg = f"`Professor Ironwood`: Right! These guys! Okay, here are your choices {name}!"
        await self.client.send_message(channel, msg)

        poke1 = await MonsterSpawner().spawn_at_level(1, 5)
        poke2 = await MonsterSpawner().spawn_at_level(4, 5)
        poke3 = await MonsterSpawner().spawn_at_level(7, 5)

        poke_list = [poke1, poke2, poke3]

        prompt_list = [x.identifier for x in poke_list]

        self.log.info(f"{self.trainer.trainer_id} Prompting for a Pokemon to use")
        while 1:
            prompt_question = "Which pokemon would you like?"
            selection = await self.client.select_prompt(channel, prompt_question, prompt_list, user=user)

            prompt = f"You wanted {prompt_list[selection]}, is that right?"
            if await self.client.confirm_prompt(channel, prompt, user=user):
                break
            self.log.info(f"{self.trainer.trainer_id} User selected {prompt_list[selection]},"
                          " but didn't like that selection.")


        self.log.info(f"{self.trainer.trainer_id} User selected {prompt_list[selection]}.")

        await self.trainer.party.add(poke_list[selection])

        await asyncio.sleep(1.5)
        await self.client.send_typing(channel)
        await asyncio.sleep(2)
        msg = f"`Professor Ironwood`: Here you go! Enjoy your adventures with {poke_list[selection].name}"
        await self.client.send_message(channel, msg)
        self.log.info(f"{self.trainer.trainer_id} Was issued their pokemon and saved.")


        # We are done, die!
        self.alive = False
