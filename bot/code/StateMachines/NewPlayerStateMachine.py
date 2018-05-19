
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


    async def run(self):
        """Run through the player creation process.
        """
        self.started = True
        self.log.info("Begin our run")
        try:
            await self._run()
        except Exception:
            self.log.exception("Something went wrong...")
            await League().deregister(self.trainer.user_id, self.trainer.server_id)

    async def _run(self):

        self.log.info("Creating a new player!")


        user = await self.client.get_user_info(self.trainer.user_id)
        await self.client.start_private_message(user)

        for channel in self.client.private_channels:
            if channel.user == user:
                break

        msg = "Welcome to the Pokemon League!"
        await self.client.send_message(channel, msg)

        prompt = f"Are you ready to begin?"
        response = await self.client.confirm_prompt(channel, prompt, user=user, timeout=60 * 5, clean_up=False)
        if response is not True:
            raise ValueError("User didn't answer that they were ready to go, abort!")

        await asyncio.sleep(1.5)
        await self.client.send_typing(channel)
        await asyncio.sleep(4)

        msg = "You are in for such a huge adventure!"
        await self.client.send_message(channel, msg)

        await asyncio.sleep(1.5)
        await self.client.send_typing(channel)
        await asyncio.sleep(4)

        msg = "Before we begin..."
        await self.client.send_message(channel, msg)

        while 1:
            name = await self.client.text_prompt(channel, "What is your name?", user=user)
            self.log.info(f"Got response of name='{name}'")

            prompt = f"You name is {name}, is that right?"
            response = await self.client.confirm_prompt(channel, prompt, user=user, timeout=30, clean_up=False)

            if response:
                break

        self.trainer.nickname = name

        await asyncio.sleep(1.5)
        await self.client.send_typing(channel)
        await asyncio.sleep(5)
        msg = f"Okay {name}, let's get you started!"
        await self.client.send_message(channel, msg)

        await asyncio.sleep(1.5)
        await self.client.send_typing(channel)
        await asyncio.sleep(5)
        msg = "Where did I keep those things?"
        await self.client.send_message(channel, msg)

        await asyncio.sleep(1.5)
        await self.client.send_typing(channel)
        await asyncio.sleep(2)
        msg = "Up here?"
        await self.client.send_message(channel, msg)

        await asyncio.sleep(1.5)
        await self.client.send_typing(channel)
        await asyncio.sleep(7)
        msg = "Nope!"
        await self.client.send_message(channel, msg)

        await asyncio.sleep(1.5)
        await self.client.send_typing(channel)
        await asyncio.sleep(2)
        msg = "*Looks at the table*"
        await self.client.send_message(channel, msg)

        await asyncio.sleep(1.5)
        await self.client.send_typing(channel)
        await asyncio.sleep(2)
        msg = f"Right! These guys! Okay, here are your choices {name}!"
        await self.client.send_message(channel, msg)

        poke1 = await MonsterSpawner().spawn_at_level(1, 5)
        poke2 = await MonsterSpawner().spawn_at_level(4, 5)
        poke3 = await MonsterSpawner().spawn_at_level(7, 5)

        poke_list = [poke1, poke2, poke3]

        prompt_list = [x.identifier for x in poke_list]

        while 1:
            prompt_question = "Which pokemon would you like?"
            selection = await self.client.select_prompt(channel, prompt_question, prompt_list, user=user)

            prompt = f"You wanted {prompt_list[selection]}, is that right?"
            if await self.client.confirm_prompt(channel, prompt, user=user):
                break

        await asyncio.sleep(1.5)
        await self.client.send_typing(channel)
        await asyncio.sleep(2)
        msg = f"Listen, I'm kinda not sure how to give this to you? I'm a bit of a stupid bot right now..."\
            " Sorry about that..."
        await self.client.send_message(channel, msg)

        await asyncio.sleep(1.5)
        await self.client.send_typing(channel)
        await asyncio.sleep(2)
        msg = f"Either way, I hope you have a good adventure, {name}! (~~God, what a stupid name...~~)"
        await self.client.send_message(channel, msg)

        # We are done, die!
        self.alive = False
