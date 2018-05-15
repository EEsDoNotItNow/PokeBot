
import re
import uuid

from .States import GameSessionStates
from ..Log import Log
from ..Client import Client



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


    async def command_proc(self, message):
        """Player in a session has issued a command, handle it.
        """
        self.log.info(f"Command from player seen: '{message.content}'")
        self.log.info(f"Session ID: {self.session_uuid}")

        match_obj = re.match("> ?card( <@!?(?P<mention>[0-9]+)>)?", message.content) or re.match("> ?trainer ?$", message.content)
        if match_obj:
            self.log.info(match_obj.groups())
            self.log.info(match_obj.group(mention))

            await self.client.send_message(message.channel, embed=await self.trainer.em())

            return
