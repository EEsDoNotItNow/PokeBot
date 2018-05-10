

import discord
import datetime
import dateutil.parser

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


    async def get_trainer_card(self):
        em = discord.Embed()

        server = self.client.get_server(self.server_id)
        member = server.get_member(self.user_id)

        em.title = "Trainer Card"

        em.set_author(name=self.nickname)

        em.add_field(name="Level", value=0)

        em.add_field(name="Pokedex", value="15/75")

        em.add_field(name="Leader", value="Bolt (Pikachu) L.25")

        em.timestamp = self.created_on

        return em