
import uuid
import datetime

from ..SQL import SQL
from ..Log import Log
from .Trainer import Trainer
from ..Client import Client


class League:

    def __init__(self, server_id):
        self.sql = SQL()
        self.log = Log()
        self.client = Client()
        pass


    async def get_trainer(self, user_id, server_id):
        # Return player, or None if not registered
        cur = self.sql.cur

        cmd = "SELECT trainer_id FROM trainers WHERE server_id=:server_id AND user_id=:user_id"
        value = cur.execute(cmd, locals()).fetchone()
        if value is None:
            return None

        return Trainer(value['trainer_id'])


    async def register(self, user_id, server_id):
        """Register with the league!
        """

        trainer_id = await Trainer.generate_trainer_tables(user_id, server_id)

        return await self.get_trainer(user_id, server_id)


    async def deregister(self, user_id, server_id):
        """Register with the league!
        """

        cmd = "SELECT trainer_id FROM trainers WHERE server_id=:server_id AND user_id=:user_id"
        value = cur.execute(cmd, locals()).fetchone()
        if value is None:
            return False

        # Sorry dude, you are getting BALETED
        cmd = "DELETE FROM trainers WHERE server_id=:server_id AND user_id=:user_id"
        cur.execute(cmd, locals())
        await self.sql.commit()


