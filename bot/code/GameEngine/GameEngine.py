
import re

from ..Log import Log
from ..Client import Client
from ..Player import Trainer, League

class GameEngine:

    def __init__(self):
        self.log = Log()
        self.client = Client()
        pass


    async def on_message(self, message):        

        self.log.info(f"Saw message: {message.content}")

        match_obj = re.match("<@!?(?P<id>\d+)>", message.content)
        if match_obj and match_obj.group('id')==self.client.user.id:
            self.log.info("Saw a command, handle it!")

        match_obj = re.match("^>", message.content)
        if match_obj :
            self.log.info("Saw a play command, handle it!")
            await self.command_proc(message)


    async def on_ready(self):
        self.log.info("GameEngine, ready to recieve commands!")
        await League.table_setup()


    async def on_resumed(self):
        self.log.info("GameEngine, ready to recieve commands!")
        pass


    async def command_proc(self, message):

        match_obj = re.match("> *register *$", message.content)
        if match_obj:
            # Create a basic trainer object
            trainer = await League(message.server.id).get_trainer(message.author.id, message.server.id)
            if trainer is not None:
                await self.client.send_message(message.channel, "Error, I cannot re-register you!")
                return

            # We are good to register them!
            trainer = await League(message.server.id).register(message.author.id, message.server.id)

            em = await trainer.get_trainer_card()
            # await self.client.send_message(message.channel, f"Registered: {trainer}")

            await self.client.send_message(message.channel, embed=em)

            return
