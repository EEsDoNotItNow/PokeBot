
import re

from ..Log import Log
from ..Client import Client
from ..Player import League

from ..Session import SessionManager



class GameEngine:

    def __init__(self):
        self.log = Log()
        self.client = Client()
        self.session_manager = SessionManager()
        self.ready = False
        pass


    async def on_message(self, message):
        if not self.ready:
            return

        self.log.debug(f"Saw message: {message.content}")

        match_obj = re.match("^>", message.content)
        if match_obj:
            self.log.info("Saw a command, handle it!")
            await self.command_proc(message)


    async def on_ready(self):
        self.log.info("GameEngine, ready to recieve commands!")
        bot_spam = self.client.get_channel('443892226486042638')
        await self.client.send_message(bot_spam, "ready!")
        self.ready = True


    async def on_resumed(self):
        self.log.info("GameEngine, ready to recieve commands!")
        pass


    async def command_proc(self, message):
        """Handle specific commands, or pass to the session_manager
        """

        match_obj = re.match("> *register *$", message.content)
        if match_obj:
            # Create a basic trainer object
            if message.server is None:
                await self.client.send_message(message.channel,
                                               "Sorry, you must register in a server! I cannot register you over DMs!")
                return

            trainer = await League().get_trainer(message.author.id, message.server.id)
            if trainer is not None:
                await self.client.send_message(message.channel, "Error, I cannot re-register you!")
                return

            # We are good to register them!
            trainer = await League().register(message.author.id, message.server.id)

            em = await trainer.get_trainer_card()
            # await self.client.send_message(message.channel, f"Registered: {trainer}")

            await self.client.send_message(message.channel, embed=em)

            return

        match_obj = re.match("> *deregister *$", message.content)
        if match_obj:
            # Create a basic trainer object
            result = await League().deregister(message.author.id, message.server.id)
            if result:
                await self.client.send_message(message.channel,
                                               f"The Discord League is sorry to see you go, <@!{message.author.id}>")  # noqa: E501
            else:
                await self.client.send_message(message.channel,
                                               f"The Discord League doesn't seem to have you registered, <@!{message.author.id}>")  # noqa: E501

            return

        match_obj = re.match(">spawn", message.content)
        if match_obj:
            from ..Pokemon import MonsterSpawner

            poke = await MonsterSpawner().spawn_random()

            await self.client.send_message(message.channel,
                                           embed=await poke.em())
            self.log.info("Finished spawn command")

            return

        match_obj = re.match(">test (.*)", message.content)
        if match_obj:
            from ..CommandProcessor import DiscordArgumentParser
            import shlex
            parser = DiscordArgumentParser()
            try:
                results = parser.parse_args(shlex.split(match_obj.group(1)))
            except Exception as e:
                await self.client.send_message(message.channel, e)
                return

            await self.client.send_message(message.channel, results)

            self.log.info("Finished test command")

            return

        match_obj = re.match("> ?emojidecode (.*)$", message.content)
        if match_obj:
            self.log.info(match_obj.groups())

            string = match_obj.group(1).encode('unicode_escape')
            await self.client.send_message(message.channel, f"{string}: {string.decode('unicode-escape')}")
            return

        # If we failed to trigger a command, we need to ask the session manager to handle it!
        await self.session_manager.command_proc(message)
