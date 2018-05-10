
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


    @classmethod
    async def table_setup(cls):
        """Setup any SQL tables needed for this class
        """
        log = Log()
        log.info("Check to see if trainers exists.")
        sql = SQL()
        if not await sql.table_exists("trainers"):
            log.info("Create trainers table")
            cur = sql.cur
            cmd = """
                CREATE TABLE trainers 
                (
                    trainer_id TEXT NOT NULL,
                    user_id TEXT NOT NULL, 
                    server_id TEXT NOT NULL,
                    nickname TEXT,
                    created_on TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """
            cur.execute(cmd)
            await sql.commit()



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

        user = self.client.get_server(server_id).get_member(user_id)

        name = user.nick if user.nick else user.name

        cmd = """INSERT INTO trainers 
            (trainer_id, 
            user_id, 
            server_id, 
            nickname,
            created_on)
            VALUES
            (:trainer_id, :user_id, :server_id, :name, :now)"""

        trainer_id = str(uuid.uuid4())
        now = datetime.datetime.now()

        ret = self.sql.cur.execute(cmd, locals()).fetchone()

        return await self.get_trainer(user_id, server_id)


