
from ..Client import Client
from ..Log import Log
from ..Player import League
from ..Singleton import Singleton

from .Session import Session

class SessionManager(metaclass=Singleton):
    """Given information, return active or new sessions
    """
    sessions = []


    def __init__(self):
        self.log = Log()
        self.client = Client()


    async def command_proc(self, message):
        """Find, or load, the correct session
        """
        self.log.info(f"Saw command to process: {message.content}")

        session = await self.get_session(message)

        if session == None:
            self.log.warning(f"No session found! What?!")
            return

        self.log.info(f"Got session: {session}")

        await session.command_proc(message)

        return


    async def get_session(self, message):

        trainers = await League().get_trainer(message.author.id)
        self.log.info(f"Got trainer list: {trainers}")

        if trainers == None:
            await self.client.send_message(message.channel, "I'm sorry, I don't seem to have you marked as a trainer! Perhaps you need to `>register`?")
            return None

        # Lookup Trainer
        # We don't always know if we have a server ID, so just lookup everyone and we will find the only active session

        for trainer in trainers:
            for session in self.sessions:
                if session.trainer == trainer:
                    return session
                else:
                    self.log.info(f"{session.trainer} != {trainer}")

        # Active sessions didn't work, check the inactive ones!
        pass

        # Inactive session not found, return a NEW session
        if len(trainers) == 1:
            self.log.info("No session found, create a new one")
            session = Session(trainers[-1])
            self.sessions.append(session)
            return session
        pass
