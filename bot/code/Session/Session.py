
import datetime
import re
import uuid

from ..Client import Client
from ..Log import Log
from ..SQL import SQL
from ..Player import TrainerStates as TS
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

        # Information printing commands can always be run

        match_obj = re.match("> ?s(?:tatus)?$", message.content)
        if match_obj:

            if self.trainer.state == TS.WALKING:

                # Safe to update, lets see where we are!
                await self.trainer.tick()
                msg = f"You are walking! You have about {self.trainer.destination_distance:,.0f} to go!"

            elif self.trainer.state == TS.IDLE:
                msg = "You are `idle`. Maybe you could try `>walk`?"

            else:
                msg = f"You are in a state I don't know about yet!"\
                    f" Please file a bug report! State: {TS(self.trainer.state).name}"


            await self.client.send_message(message.channel,
                                           msg)

            self.log.info("Command Complete")
            return

        match_obj = \
            re.match("> ?card( <@!?(?P<mention>[0-9]+)>)?$", message.content) or \
            re.match("> ?trainer( <@!?(?P<mention>[0-9]+)>)?$", message.content)
        if match_obj:
            self.log.info(match_obj.groups())
            self.log.info(match_obj.group('mention'))

            await self.client.send_message(message.channel, embed=await self.trainer.em())

            return

        match_obj = re.match("> ?stat(?:s)?(?: (?P<stat>\w+))?$", message.content)
        if match_obj:
            self.log.info(match_obj.groups())
            self.log.info(match_obj.group('stat'))

            cur = self.sql.cur

            cmd = f"SELECT * FROM trainer_stats WHERE trainer_id=:trainer_id"
            values = cur.execute(cmd, self.trainer.__dict__).fetchone()

            msg = "```\n"
            msg += f"Steps Taken: {values['steps_taken']:,d}\n"
            msg += "```"

            await self.client.send_message(message.channel, msg)

            return

        match_obj = re.match("> ?loc(?:ation)?$", message.content)
        if match_obj:
            self.log.info(match_obj.groups())
            location_tuple = await self.trainer.get_location()
            current_zone = await World().get_zone(location_tuple[1])
            await self.client.send_message(message.channel,
                                           f"You are in {current_zone}"
                                           )

            return

        match_obj = re.match("> ?map$", message.content)
        if match_obj:
            self.log.info(match_obj.groups())
            world = World()
            location_tuple = await self.trainer.get_location()
            current_zone = await world.get_zone(location_tuple[1])

            _map = f"```\nYou are currently in {current_zone}. From here, you can get to the following locations:\n"
            for linked_zone_id in current_zone.links:
                zone = await world.get_zone(linked_zone_id)
                _map += f"   {zone}\n"
            _map += "```"
            await self.client.send_message(message.channel, _map)

            return

        match_obj = re.match("> ?worldmap$", message.content)
        if match_obj:
            self.log.info(match_obj.groups())
            location_tuple = await self.trainer.get_location()

            await self.client.send_message(message.channel, "This feature isn't implemented yet!")

            return

        match_obj = re.match("> ?regionmap$", message.content)
        if match_obj:
            self.log.info(match_obj.groups())
            location_tuple = await self.trainer.get_location()

            await self.client.send_message(message.channel, "This feature isn't implemented yet!")

            return

        match_obj = re.match("> ?stop$", message.content)
        if match_obj:
            self.log.info(match_obj.groups())
            # Check for valid states that we can stop from
            valid_stopable_states = [TS.IDLE, TS.BREEDING, TS.HATCHING, TS.RESTING, TS.TRAINING, TS.WORKING,
                                     TS.WALKING, TS.WALKING_IN_GRASS, TS.BIKING, TS.RUNNING, TS.TRADING,
                                     TS.SHOPPING, TS.SOMEONES_PC]
            if TS(self.trainer.state) in valid_stopable_states:
                self.trainer.state = TS.IDLE
                # TODO: This is an ugly ugly hack, we need to cleanup everything else
                # that MIGHT be going on first!

            return

        match_obj = re.match("> ?find$", message.content)
        if match_obj:
            self.log.info(match_obj.groups())
            # Check for valid states that we can stop from
            valid_stopable_states = [TS.IDLE, TS.BREEDING, TS.HATCHING, TS.RESTING, TS.TRAINING, TS.WORKING,
                                     TS.WALKING, TS.WALKING_IN_GRASS, TS.BIKING, TS.RUNNING, TS.TRADING,
                                     TS.SHOPPING, TS.SOMEONES_PC]
            if TS(self.trainer.state) in valid_stopable_states:
                self.trainer.state = TS.IDLE
                # TODO: This is an ugly ugly hack, we need to cleanup everything else
                # that MIGHT be going on first!

            return

        match_obj = re.match("> ?walk$", message.content)
        if match_obj:
            self.log.info(match_obj.groups())

            # Can we walk?
            if self.trainer.state not in [TS.IDLE, ]:
                msg = f"You cannot do that right now! You are {TS(self.trainer.state).name}"
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

            prompt_question = f"You are in {current_zone}. Which zone do you want to travel too?"
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
                                           f"<@!{message.author.id}> began to walk to {linked_zones[selection]}"
                                           )
            return

        self.log.warning(f"Saw a command ({message.content}), which did not match any current commands.")
