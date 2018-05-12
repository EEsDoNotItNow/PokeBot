

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
        self.user_id =  values['user_id']
        self.server_id =  values['server_id']

        cmd = "SELECT * FROM trainer_stats WHERE trainer_id = :trainer_id"
        values = self.sql.cur.execute(cmd, locals()).fetchone()

        self.stats = dict(values)



    @classmethod
    async def generate_trainer_tables(cls, user_id, server_id):

        user = Client().get_server(server_id).get_member(user_id)

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

        cmd = """INSERT INTO trainer_stats
        (trainer_id)
        VALUES
        (:trainer_id)"""
        sql.cur.execute(cmd, locals())
        await sql.commit()



    async def get_trainer_card(self):
        em = discord.Embed()

        server = self.client.get_server(self.server_id)
        member = server.get_member(self.user_id)

        em.title = "Trainer Card"

        em.set_author(name=self.nickname)

        em.add_field(name="Pokecoin", value=f"{self.stats['pokecoin']:,.2f}")

        em.add_field(name="Level", value=f"{self.level:,d}")

        em.timestamp = self.created_on

        return em


    @property 
    def level(self):
        return int(numpy.sqrt(self.stats['xp']))
