
from ..Log import Log
from ..Singleton import Singleton

class SessionManager(metaclass=Singleton):
    """Given information, return active or new sessions
    """
    sessions = []


    def __init__(self):
        self.log = Log()


    async def command_proc(self, message):
        """Find, or load, the correct session 
        """
        self.log.info(f"Saw command to process: {message.content}")

        # Check our active sessions 
        pass

        # Check our inaction sessions
        pass

        # Create a new session
        pass

        return
