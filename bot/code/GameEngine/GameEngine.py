
import asyncio
import re

from ..Log import Log
from ..Client import Client
from ..Player import Trainer, League
from ..SQL import SQL

from ..Pokemon import MonsterSpawner, Pokemon
from ..World import World

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
        admin = await self.client.get_user_info(205161476204396544)
        await self.client.send_message(admin, "ready!")


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

        match_obj = re.match("> *deregister *$", message.content)
        if match_obj:
            # Create a basic trainer object
            result =  await League(message.server.id).deregister(message.author.id, message.server.id)
            if result:
                await self.client.send_message(message.channel, f"The Discord League is sorry to see you go, <@!{message.author.id}>")
            else:
                await self.client.send_message(message.channel, f"The Discord League doesn't seem to have you registered, <@!{message.author.id}>")

            return

        match_obj = re.match("> *spawn ?(\d+)?$", message.content)
        if match_obj:
            self.log.info(match_obj.groups())
            spawner = MonsterSpawner()
            poke = await spawner.spawn_random()
            self.log.info(poke)

            await self.client.send_message(message.channel, "Demo Spawn Example (very random)", embed=await poke.em(debug=True))

            return


        match_obj = re.match(">test$", message.content)
        if match_obj:
            self.log.info(match_obj.groups())
            trainer = await League(message.server.id).get_trainer(message.author.id, message.server.id)
            if trainer is None:
                await self.client.send_message(message.channel, "Sorry, you need to register first!")
                return

            stats_dict = {}
            stats_dict['commands'] = 1
            await trainer.log_stats(stats_dict)
            self.log.info("Finished test command")

            return


        match_obj = re.match(">map$", message.content)
        if match_obj:
            self.log.info(match_obj.groups())
            world = World()
            await world.load()
            await world.debug(message.channel)

            return

