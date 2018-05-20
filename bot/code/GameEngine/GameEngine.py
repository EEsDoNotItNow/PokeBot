
import asyncio
import numpy as np
import re
import shlex

from ..Client import Client
from ..CommandProcessor import DiscordArgumentParser
from ..CommandProcessor.exceptions import NoValidCommands, HelpNeeded
from ..Log import Log
from ..Player import League
from ..Pokemon import MonsterSpawner
from ..Session import SessionManager
from ..SQL import SQL



class GameEngine:


    def __init__(self):
        self.sql = SQL()
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
            await self.log_command(message)
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
        sub_parser.add_argument("--fast",
                                action='store_true')
        sub_parser.set_defaults(subCMD='>register',
                                cmd=self._cmd_register)


        sub_parser = sp.add_parser('>deregister',
                                   description='Deregister self with the Pokemon League')
        sub_parser.set_defaults(subCMD='>deregister',
                                cmd=self._cmd_deregister)


        sub_parser = sp.add_parser('>spawn',
                                   description="Spawn a random Poke")
        sub_parser.add_argument("pokemon_id",
                                type=int,
                                nargs='?')
        sub_parser.add_argument("level",
                                type=int,
                                choices=range(1, 101),
                                metavar="1-100",
                                help="Level of pokemon to spawn",
                                default=None,
                                nargs='?')
        sub_parser.set_defaults(subCMD='>spawn',
                                cmd=self._cmd_spawn)


        sub_parser = sp.add_parser('>test',
                                   description='test something')
        sub_parser.set_defaults(subCMD='>test',
                                cmd=self._cmd_test)


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
                await results.cmd(results)
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

    async def _cmd_register(self, args):
        message = args.message
        if message.server is None:
            await self.client.send_message(message.channel,
                                           "Sorry, you must register in a server! I cannot register you over DMs!")

        self.log.info("Spawn a player registration.")
        await self.session_manager.spawn_registration_session(args)
        self.log.info("Fin spawn a player registration.")
        return


    async def _cmd_deregister(self, args):
        message = args.message
        # Create a basic trainer object
        self.log.info("Deleting a Trainer.")
        self.log.info("Remove all sessions")
        await self.session_manager.delete_session(message)
        self.log.info("Remove from League")
        result = await League().deregister(message.author.id, message.server.id)
        self.log.info(f"Removal result: {result}")
        if result:
            # Remove any sessions with this trainer.
            await self.client.send_message(message.channel,
                                           f"The Discord League is sorry to see you go, <@!{message.author.id}>")  # noqa: E501
        else:
            await self.client.send_message(message.channel,
                                           f"The Discord League doesn't seem to have you registered, <@!{message.author.id}>")  # noqa: E501
        return


    async def _cmd_spawn(self, args):
        message = args.message

        if hasattr(args, "pokemon_id") and args.pokemon_id is not None:
            if hasattr(args, "level") and args.level is not None:
                level = args.level
            else:
                level = np.random.randint(1, 100)
            poke = await MonsterSpawner().spawn_at_level(args.pokemon_id, level)
        else:
            poke = await MonsterSpawner().spawn_random()

        await self.client.send_message(message.channel,
                                       embed=await poke.em())
        self.log.info("Finished spawn command")
        return


    async def _cmd_emojidecode(self, args):
        message = args.message

        for emoji in args.emoji:
            await self.client.send_message(message.channel, f"'{emoji}': {emoji.encode('unicode_escape')}")
        return


    async def _cmd_test(self, args):
        message = args.message

        from ..Client import EmojiMap
        em = EmojiMap()

        for key in em.emojis:
            await asyncio.sleep(1)
            await self.client.send_message(message.channel, f"`{key}`: {em(key)}")

    async def log_command(self, message):

        message_id = message.id
        channel_id = message.channel.id if message.channel else None
        author_id = message.author.id
        created_at = message.timestamp.timestamp()
        content = message.content
        cmd = """
            INSERT INTO command_log
            (
                message_id,
                channel_id,
                author_id,
                created_at,
                content
            ) VALUES (
                :message_id,
                :channel_id,
                :author_id,
                :created_at,
                :content
            )"""
        self.sql.cur.execute(cmd, locals())
        await self.sql.commit(now=True)
