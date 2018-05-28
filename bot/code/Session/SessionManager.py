
import asyncio

from ..Client import Client
from ..Log import Log
from ..Player import League
from ..Player import TrainerStates as TS
from ..Singleton import Singleton
from ..UserInterfaces import NewPlayerUserInterface

from .Session import Session



class SessionManager(metaclass=Singleton):
    """Given information, return active or new sessions
    """
    sessions = []


    def __init__(self):
        self.log = Log()
        self.client = Client()


    async def on_ready(self):
        self.log.info("Starting the tick loop!")
        asyncio.ensure_future(self.tick())
        self.log.info("tick loop started")
        pass


    async def tick(self):
        """Tick current game state
        """
        while 1:
            await asyncio.sleep(5)
            self.log.debug("Tick")
            for session in self.sessions:
                asyncio.ensure_future(session.tick())

            pruned_sessions = [x for x in SessionManager.sessions if not x.alive]
            for session in pruned_sessions:
                await session.save()
                self.log.debug(f"Pruned session: {session}")
            SessionManager.sessions = [x for x in SessionManager.sessions if x.alive]


    async def command_proc(self, message):
        """Find, or load, the correct session
        """
        self.log.info(f"Saw command to process: {message.content}")

        session = await self.get_session(message)

        if session is None:
            self.log.warning(f"No session found! What?!")
            return

        self.log.info(f"Got session: {session}")

        await session.command_proc(message)

        return


    async def delete_session(self, message):

        trainers = await League().get_trainer(message.author.id)

        if trainers is None:
            await self.client.send_message(message.channel,
                                           "I'm sorry, I don't seem to have you marked as a trainer! "
                                           "Perhaps you need to `>register`?")
            return False

        # Lookup Trainer
        # We don't always know if we have a server ID, so just lookup everyone and we will find the only active session

        for trainer in trainers:
            for session in self.sessions:
                if session.trainer == trainer:
                    self.log.info(f"Deleted session {session}")
                    self.sessions.remove(session)
                    del session
                    return True
        return False


    async def get_session(self, message):

        trainers = await League().get_trainer(message.author.id)

        if trainers is None:
            await self.client.send_message(message.channel,
                                           "I'm sorry, I don't seem to have you marked as a trainer! "
                                           "Perhaps you need to `>register`?")
            return None

        # Lookup Trainer
        # We don't always know if we have a server ID, so just lookup everyone and we will find the only active session

        for trainer in trainers:
            for session in self.sessions:
                if session.trainer == trainer:
                    return session

        # Active session not found, return a NEW session
        if len(trainers) == 1:
            self.log.info("No session found, create a new one")
            session = Session(trainers[-1])
            self.sessions.append(session)
            return session
        pass


    async def spawn_registration_session(self, args):
        # Create a basic trainer object
        message = args.message
        trainer = await League().get_trainer(message.author.id, message.server.id)
        if trainer is not None:
            self.log.warning("We saw a trainer request to register when they were already in the league!")
            await self.client.send_message(message.channel, "Error, I cannot re-register you!")
            return

        # We are good to register them!
        trainer = await League().register(message.author.id, message.server.id)

        trainer.state = TS.IN_SCRIPT

        # I assume that we do not have an active session already, as this player isn't registered.
        session = Session(trainer)
        session.state_machine = NewPlayerUserInterface(trainer, args)
        self.sessions.append(session)
        msg = "Your request for registration is in the mail! Please wait 6 to 8 weeks for delivery!"
        await self.client.send_message(message.channel, msg)

        return
