
import asyncio

from ..Client import Client
from ..SQL import SQL
from ..Log import Log
from ..Player import League

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

        await asyncio.sleep(1)
        await self.client.send_typing(channel)
        await asyncio.sleep(3)

        msg = "You are in for such a huge adventure!"
        await self.client.send_message(channel, msg)

        await asyncio.sleep(1)
        await self.client.send_typing(channel)
        await asyncio.sleep(3)

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


        await asyncio.sleep(1)
        await self.client.send_typing(user)
        await asyncio.sleep(10)
        msg = "Oh shit! I don't have any pokemon to give you yet. Sorry about that! Umm, you can try `>walk`ing around"\
            " a bit?"
        await self.client.send_message(user, msg)

        # We are done, die!
        self.alive = False
