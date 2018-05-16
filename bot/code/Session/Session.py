
import re
import uuid

from .States import GameSessionStates
from ..Log import Log
from ..Client import Client
from ..World import World



class Session:
    """Game play session to manage player interactions
    """


    def __init__(self, trainer, session_uuid=None):
        self.trainer = trainer

        self.log = Log()
        self.client = Client()

        self.state = GameSessionStates.IDLE

        self.trainer = trainer

        if session_uuid is None:
            self.session_uuid = uuid.uuid4()
        else:
            self.session_uuid = session_uuid

        # Mark ourselves as alive. This Session will self terminate if conditions are met.
        self.alive = True


    async def command_proc(self, message):
        """Player in a session has issued a command, handle it.
        """
        self.log.info(f"Command from player seen: '{message.content}'")
        self.log.info(f"Session ID: {self.session_uuid}")

        match_obj = re.match("> ?card( <@!?(?P<mention>[0-9]+)>)?$", message.content) or \
            re.match("> ?trainer( <@!?(?P<mention>[0-9]+)>)?$", message.content)
        if match_obj:
            self.log.info(match_obj.groups())
            self.log.info(match_obj.group('mention'))

            await self.client.send_message(message.channel, embed=await self.trainer.em())

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


        match_obj = re.match("> ?walk$", message.content)
        if match_obj:
            self.log.info(match_obj.groups())
            world = World()
            location_tuple = await self.trainer.get_location()
            current_zone = await world.get_zone(location_tuple[1])

            linked_zone_ids = []
            linked_zones = []
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

            self.trainer.current_zone_id = linked_zone_ids[selection]
            await self.trainer.save()

            location_tuple = await self.trainer.get_location()
            current_zone = await World().get_zone(location_tuple[1])
            await self.client.send_message(message.channel,
                                           f"You are in {current_zone}"
                                           )
            return
