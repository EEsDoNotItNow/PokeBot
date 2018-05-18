
import datetime
import shlex
import uuid

from ..Client import Client
from ..CommandProcessor import DiscordArgumentParser
from ..CommandProcessor.exceptions import NoValidCommands, HelpNeeded
from ..Log import Log
from ..Player import TrainerStates as TS
from ..SQL import SQL
from ..World import World



class Session:
    """Game play session to manage player interactions
    """


    def __init__(self, trainer, session_uuid=None):
        self.trainer = trainer

        self.client = Client()
        self.log = Log()
        self.sql = SQL()

        self.trainer = trainer

        if session_uuid is None:
            self.session_uuid = uuid.uuid4()
        else:
            self.session_uuid = session_uuid

        # Mark ourselves as alive. This Session will self terminate if conditions are met.
        self.alive = True
        self.last_command = datetime.datetime.now()
        self.processing_command = False


    def __repr__(self):
        return f"Session({self.session_uuid})"


    async def save(self):
        await self.trainer.save()


    async def tick(self):
        """Tick current game state
        """

        if not self.alive:
            return

        self.log.debug(f"Session {self.session_uuid}, ticking.")

        await self.trainer.tick()

        if datetime.datetime.now() - self.last_command > datetime.timedelta(minutes=15):
            self.alive = False


    async def command_proc(self, message):
        if self.processing_command:
            self.log.warning(f"Saw a command ({message.content}) while we were already processing!")
            return
        self.processing_command = True

        self.log.info(f"Command from player seen: '{message.content}'")
        self.log.info(f"Session ID: {self.session_uuid}")
        self.last_command = datetime.datetime.now()
        try:
            await self._command_proc(message)
        finally:
            self.processing_command = False


    async def _command_proc(self, message):
        """Player in a session has issued a command, handle it.
        """
        parser = DiscordArgumentParser(description="Session Command Processor", prog="")
        parser.set_defaults(message=message)
        sps = parser.add_subparsers(title="commands")


        sp = sps.add_parser('>status',
                            description='Current game status (generic)',
                            aliases=['>s'],
                            prog=">status",
                            add_help=True)
        sp.set_defaults(cmd=self._cmd_status,
                        subCMD='>status',)


        sp = sps.add_parser('>card',
                            description='Print your trainer card',
                            aliases=['>trainer'],
                            add_help=True)
        sp.set_defaults(cmd=self._cmd_card,
                        subCMD='>card',)


        sp = sps.add_parser('>stats',
                            description='Current game stats (generic)',
                            add_help=True)
        sp.set_defaults(cmd=self._cmd_stats,
                        subCMD='>stats',)


        sp = sps.add_parser('>location',
                            aliases=['>loc'],
                            description='Show info about this location',
                            add_help=True)
        sp.set_defaults(cmd=self._cmd_location,
                        subCMD='>location',)


        sp = sps.add_parser('>map',
                            description='Print the local map',
                            add_help=True)
        sp.set_defaults(cmd=self._cmd_map,
                        subCMD='>map',)


        sp = sps.add_parser('>stop',
                            description='Stop what you are doing',
                            add_help=True)
        sp.set_defaults(cmd=self._cmd_stop,
                        subCMD='>stop',)


        sp = sps.add_parser('>find',
                            description='WIP',
                            add_help=True)
        sp.set_defaults(cmd=self._cmd_find,
                        subCMD='>find',)


        sp = sps.add_parser('>walk',
                            description='Walk to a zone',
                            add_help=True)
        sp.set_defaults(cmd=self._cmd_walk,
                        subCMD='>walk',)


        try:
            self.log.info("Parse Arguments")
            results = parser.parse_args(shlex.split(message.content))
            if type(results) == str:
                await self.client.send_message(message.channel, results)
                return
            elif hasattr(results, 'cmd'):
                # await self.client.send_message(message.channel, results)
                self.log.info(results)
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
            self.log.warning(f"Saw bad user input: {message.content}. Notifying user of '{e}'.")
            msg = f"{e}. You can add `-h` or `--help` to any command to get more help!"
            await self.client.send_message(message.channel, msg)
            return

        # Information printing commands can always be run
        self.log.warning(f"Saw a command ({message.content}), which did not match any current commands.")
        return


    async def _cmd_status(self, message):
        # TODO: STatus

        if self.trainer.state == TS.WALKING:
            # Safe to update, lets see where we are!
            await self.trainer.tick()
            msg = f"<@!{message.author.id}> You are walking!"\
                " You have about {self.trainer.destination_distance:,.0f} to go!"

        elif self.trainer.state == TS.WALKING_IN_GRASS:
            # Safe to update, lets see where we are!
            await self.trainer.tick()
            msg = f"<@!{message.author.id}> You are looking for local Pokemon. Good luck!"

        elif self.trainer.state == TS.IDLE:
            msg = f"<@!{message.author.id}> You are *Idle*. Maybe you could try `>walk`?"

        else:
            msg = f"<@!{message.author.id}> You are in a state I don't know about yet!"\
                f" Please file a bug report! State: {TS(self.trainer.state).name}"


        await self.client.send_message(message.channel,
                                       msg)

        self.log.info("Command Complete")
        return


    async def _cmd_card(self, message):
        # re.match("> ?card( <@!?(?P<mention>[0-9]+)>)?$", message.content) or \
        # re.match("> ?trainer( <@!?(?P<mention>[0-9]+)>)?$", message.content)

        await self.client.send_message(message.channel, embed=await self.trainer.em())

        return


    async def _cmd_stats(self, message):
        # match_obj = re.match("> ?stat(?:s)?$", message.content)

        cur = self.sql.cur

        cmd = f"SELECT * FROM trainer_stats WHERE trainer_id=:trainer_id"
        values = cur.execute(cmd, self.trainer.__dict__).fetchone()

        msg = "<@!{message.author.id}> \n```\n"
        msg += f"Steps Taken: {values['steps_taken']:,d}\n"
        msg += "```"

        await self.client.send_message(message.channel, msg)

        return


    async def _cmd_location(self, message):
        # match_obj = re.match("> ?loc(?:ation)?$", message.content)
        location_tuple = await self.trainer.get_location()
        current_zone = await World().get_zone(location_tuple[1])
        await self.client.send_message(message.channel,
                                       f"<@!{message.author.id}> You are in {current_zone}"
                                       )

        return


    async def _cmd_map(self, message):
        # match_obj = re.match("> ?map$", message.content)
        world = World()
        location_tuple = await self.trainer.get_location()
        current_zone = await world.get_zone(location_tuple[1])

        _map = f"<@!{message.author.id}> You are currently in {current_zone}."\
            " From here, you can get to the following locations:\n```\n"
        for linked_zone_id in current_zone.links:
            zone = await world.get_zone(linked_zone_id)
            _map += f"   {zone}\n"
        _map += "```"
        await self.client.send_message(message.channel, _map)

        return


    async def _cmd_worldmap(self, message):
        # match_obj = re.match("> ?worldmap$", message.content)
        # location_tuple = await self.trainer.get_location()

        await self.client.send_message(message.channel, "This feature isn't implemented yet!")

        return


    async def _cmd_regionmap(self, message):
        # match_obj = re.match("> ?regionmap$", message.content)
        # location_tuple = await self.trainer.get_location()

        await self.client.send_message(message.channel, "This feature isn't implemented yet!")

        return


    async def _cmd_stop(self, message):
        # match_obj = re.match("> ?stop$", message.content)
        # Check for valid states that we can stop from
        valid_transition_states = [TS.IDLE, TS.BREEDING, TS.HATCHING, TS.RESTING, TS.TRAINING, TS.WORKING,
                                   TS.WALKING, TS.WALKING_IN_GRASS, TS.BIKING, TS.RUNNING, TS.TRADING,
                                   TS.SHOPPING, TS.SOMEONES_PC]
        if TS(self.trainer.state) in valid_transition_states:
            self.trainer.state = TS.IDLE
            await self.trainer.save()
            msg = f"<@!{message.author.id}> You stop and wait."
            await self.client.send_message(message.channel, msg)
            # TODO: This is an ugly ugly hack, we need to cleanup everything else
            # that MIGHT be going on first!

        return


    async def _cmd_find(self, message):
        # match_obj = re.match("> ?find$", message.content)

        # Check for valid states that we can stop from
        valid_transition_states = [TS.IDLE, TS.BREEDING, TS.HATCHING, TS.RESTING, TS.TRAINING, TS.WORKING,
                                   TS.WALKING, TS.WALKING_IN_GRASS, TS.BIKING, TS.RUNNING, TS.TRADING,
                                   TS.SHOPPING, TS.SOMEONES_PC]
        if TS(self.trainer.state) in valid_transition_states:
            msg = f"<@!{message.author.id}> You cannot do that right now! This command doesn't work!"
            await self.client.send_message(message.channel, msg)

            # TODO: This is an ugly ugly hack, we need to cleanup everything else
            # that MIGHT be going on first!

        return


    async def _cmd_walk(self, message):
        # match_obj = re.match("> ?walk$", message.content)
        # Can we walk?
        valid_transition_states = [TS.IDLE, TS.BREEDING, TS.HATCHING, TS.RESTING, TS.TRAINING, TS.WORKING,
                                   TS.WALKING, TS.WALKING_IN_GRASS, TS.BIKING, TS.RUNNING, TS.SHOPPING,
                                   TS.SOMEONES_PC]
        if self.trainer.state not in valid_transition_states:
            msg = f"<@!{message.author.id}> You cannot do that right now! You are {TS(self.trainer.state).name}!"
            await self.client.send_message(message.channel, msg)
            return

        world = World()
        location_tuple = await self.trainer.get_location()
        current_zone = await world.get_zone(location_tuple[1])

        linked_zone_ids = [None, ]
        linked_zones = ["Find Pokemon"]
        for linked_zone_id in current_zone.links:
            linked_zone_ids.append(linked_zone_id)
            zone = await world.get_zone(linked_zone_id)
            linked_zones.append(zone)

        prompt_question = f"<@!{message.author.id}> You are in {current_zone}."\
            " Which zone do you want to travel too?"
        prompt_list = linked_zones
        selection = await self.client.select_prompt(message.channel,
                                                    prompt_question,
                                                    prompt_list,
                                                    user=message.author,
                                                    timeout=30,
                                                    clean_up=False)

        if selection == 0:
            self.trainer.state = TS.WALKING_IN_GRASS
        else:
            self.trainer.destination_zone_id = linked_zone_ids[selection]
            self.trainer.destination_distance = current_zone.links[linked_zone_ids[selection]]
            self.trainer.state = TS.WALKING
        self.log.info("Begin walking!")
        await self.trainer.save()

        await self.client.send_message(message.channel,
                                       f"<@!{message.author.id}> You begin to walk to {linked_zones[selection]}"
                                       )
        return
