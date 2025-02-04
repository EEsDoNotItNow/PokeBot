
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

        self.log.info(f"Saw message: {message.content}")

        match_obj = re.match("^>", message.content)
        if match_obj:
            self.log.info("Saw a play command, handle it!")
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

        match_obj = re.match(">test", message.content)
        if match_obj:
            # self.log.info(match_obj.groups())

            # prompt = "Do you like pie?"

            # response = await self.client.confirm_prompt(message.channel, prompt, user=message.author)
            # response = await self.client.select_prompt(message.channel,
            #                                            "Which is 5?",
            #                                            [1, 2, 3, 4, 5],
            #                                            user=message.author)

            response = await self.client.text_prompt(message.channel,
                                                     "Do you like pie?",
                                                     user=message.author)
            self.log.info(response)

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
