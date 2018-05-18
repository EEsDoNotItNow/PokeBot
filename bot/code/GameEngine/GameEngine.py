
import re
import shlex

from ..Client import Client
from ..CommandProcessor import DiscordArgumentParser
from ..CommandProcessor.exceptions import NoValidCommands, HelpNeeded
from ..Log import Log
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
        parser = DiscordArgumentParser(description="A Test Command", prog="", add_help=False)
        parser.set_defaults(message=message)
        sp = parser.add_subparsers()


        sub_parser = sp.add_parser('>register',
                                   description='Register self with the Pokemon League',
                                   add_help=True)
        sub_parser.set_defaults(subCMD='>register',
                                cmd=self._cmd_register)


        sub_parser = sp.add_parser('>deregister',
                                   description='Deregister self with the Pokemon League')
        sub_parser.set_defaults(subCMD='>deregister',
                                cmd=self._cmd_deregister)


        sub_parser = sp.add_parser('>spawn',
                                   description="Spawn a random Poke")
        sub_parser.set_defaults(subCMD='>spawn',
                                cmd=self._cmd_spawn)


        sub_parser = sp.add_parser('>emojidecode',
                                   description="Decode an emoji")
        sub_parser.add_argument("emoji", nargs='+')
        sub_parser.set_defaults(subCMD='>emojidecode',
                                cmd=self._cmd_emojidecode)

        try:
            self.log.info("Parse Arguments")
            results = parser.parse_args(shlex.split(message.content))
            self.log.info(results)
            if type(results) == str:
                self.log.info("Got normal return, printing and returning")
                self.log.info(type(results))
                await self.client.send_message(message.channel, results)
                return
            elif hasattr(results, 'cmd'):
                # await self.client.send_message(message.channel, results)
                await results.cmd(message)
                return
            else:
                await self.client.send_message(message.channel, results)
                msg = "Well that's funny, I don't know wha to do!"
                await self.client.send_message(message.channel, msg)
                return
        except NoValidCommands as e:
            # We didn't get a subcommand, let someone else deal with this mess!
            self.log.error("???")
            pass
        except HelpNeeded as e:
            self.log.info("TypeError Return")
            self.log.info(e)
            msg = f"{e}. You can add `-h` or `--help` to any command to get help!"
            await self.client.send_message(message.channel, msg)
            return
            pass

        self.log.critical("Command path is being refactored, commands were skipped!")
        # If we failed to trigger a command, we need to ask the session manager to handle it!
        await self.session_manager.command_proc(message)
        return


    async def _cmd_register(self, message):
        if message.server is None:
            await self.client.send_message(message.channel,
                                           "Sorry, you must register in a server! I cannot register you over DMs!")
        self.log.info("Spawn a player registration.")
        await self.session_manager.spawn_registration_session(message)
        self.log.info("Fin spawn a player registration.")
        return


    async def _cmd_deregister(self, message):
        # Create a basic trainer object
        await self.session_manager.delecte_session(message)
        result = await League().deregister(message.author.id, message.server.id)
        if result:
            # Remove any sessions with this trainer.

            await self.client.send_message(message.channel,
                                           f"The Discord League is sorry to see you go, <@!{message.author.id}>")  # noqa: E501
        else:
            await self.client.send_message(message.channel,
                                           f"The Discord League doesn't seem to have you registered, <@!{message.author.id}>")  # noqa: E501
        return


    async def _cmd_spawn(self, message):
        from ..Pokemon import MonsterSpawner

        poke = await MonsterSpawner().spawn_random()

        await self.client.send_message(message.channel,
                                       embed=await poke.em())
        self.log.info("Finished spawn command")

        return


    async def _cmd_emojidecode(self, message):

        match_obj = re.match("> ?emojidecode (.*)$", message.content)
        if match_obj:
            self.log.info(match_obj.groups())

            string = match_obj.group(1).encode('unicode_escape')
            await self.client.send_message(message.channel, f"{string}: {string.decode('unicode-escape')}")
            return
