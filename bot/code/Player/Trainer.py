

import discord
import datetime
import dateutil.parser
import uuid
import numpy

from ..Client import Client
from ..Log import Log
from ..SQL import SQL


class Trainer:

    def __init__(self, trainer_id):
        self.client = Client()
        self.log = Log()
        self.sql = SQL()

        self.trainer_id = trainer_id

        # Load info from SQL
        cmd = "SELECT * FROM trainers WHERE trainer_id = :trainer_id"
        values = self.sql.cur.execute(cmd, locals()).fetchone()

        self.nickname = values['nickname']
        self.created_on = dateutil.parser.parse(values['created_on'])
        self.user_id = values['user_id']
        self.server_id = values['server_id']

        cmd = "SELECT * FROM trainer_stats WHERE trainer_id = :trainer_id"
        values = self.sql.cur.execute(cmd, locals()).fetchone()

        self.stats = dict(values)

        self.is_zombie = False


    def __eq__(self, other):
        if type(other) != Trainer:
            raise NotImplimentedError()

        return str(self.trainer_id) == str(other.trainer_id)


    def __ne__(self, other):
        if type(other) != Trainer:
            raise NotImplimentedError()
        
        return str(self.trainer_id) != str(other.trainer_id)


    @classmethod
    async def generate_trainer_tables(cls, user_id, server_id):

        # TODO: This needs to get moved to the Trainer class

        user = Client().get_server(server_id).get_member(user_id)

        log = Log()
        sql = SQL()

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

        sql.cur.execute(cmd, locals())
        await sql.commit()

        self.log.info(f"Test before trainer write: {locals()}")
        cmd = """INSERT INTO trainer_stats
        (trainer_id)
        VALUES
        (:trainer_id)"""
        sql.cur.execute(cmd, locals())
        await sql.commit(now=True)
    


    async def log_stats(self, stats_dict):

        cmd = "PRAGMA table_info(trainer_stats)"
        cur = self.sql.cur
        data = cur.execute(cmd).fetchall()
        valid_keys = []
        for entry in data:
            valid_keys.append(entry['name'])
        self.log.info(valid_keys)

        for key in stats_dict:
            if key not in valid_keys:
                raise ValueError()
        trainer_id = self.trainer_id
        for key in stats_dict:
            value = stats_dict[key]
            cmd = f"""UPDATE trainer_stats
                      SET {key} = {key} + :value
                      WHERE trainer_id = :trainer_id"""
            cur.execute(cmd, locals())
        await self.sql.commit(now=True)
        self.log.info("log completed")


    async def get_trainer_card(self):
        em = discord.Embed()

        # server = self.client.get_server(self.server_id)
        # member = server.get_member(self.user_id)

        em.title = "Trainer Card"

        em.set_author(name=self.nickname)

        em.add_field(name="Pokecoin", value=f"{self.stats['pokecoin']:,.2f}")

        em.add_field(name="Level", value=f"{self.level:,d}")

        em.timestamp = self.created_on

        return em


    @property
    def level(self):
        return int(numpy.sqrt(self.stats['xp']))
