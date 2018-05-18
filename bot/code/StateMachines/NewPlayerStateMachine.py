
from ..Client import Client
from ..SQL import SQL
from ..Log import Log

from .BaseStateMachine import BaseStateMachine



class NewPlayerStateMachine(BaseStateMachine):
    """"Handle a new players creation process
    """

    def __init__(self, trainer):
        super().__init__()
        self.trainer = trainer

        self.client = Client()
        self.sql = SQL()
        self.log = Log()


    async def run(self):
        """Run through the player creation process.
        """
        self.started = True
        self.log.info("Creating a new player!")

        user = await self.client.get_user_info(self.trainer.user_id)

        msg = "Welcome to the Pokemon League!"
        await self.client.send_message(user, msg)

        # We are done, die!
        self.alive = False
