
import uuid

from .States import GameSessionStates
from ..Log import Log



class Session:
    """Game play session to manage player interactions
    """

    def __init__(self, trainer, session_uuid=None):
        self.trainer = trainer

        self.log = Log()

        self.state = GameSessionStates.IDLE

        if session_uuid is None:
            self.session_uuid = uuid.uuid4()
        else:
            self.session_uuid = session_uuid


    async def command_proc(self, message):
        """Player in a session has issued a command, handle it.
        """
        self.log.info(f"Command from player seen: {message.content}")
        self.log.info(f"Session ID: {self.session_uuid}")
