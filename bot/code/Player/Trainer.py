

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


    @classmethod
    async def table_setup(cls):
        """Setup any SQL tables needed for this class
        """
        log = Log()
        log.info("Check to see if trainer_stats exists.")
        sql = SQL()
        if not await sql.table_exists("trainer_stats"):
            log.info("Create trainer_stats table")
            cur = sql.cur
            cmd = """
                CREATE TABLE trainer_stats
                (
                    trainer_id TEXT NOT NULL,
                    pokecoin REAL DEFAULT 0,
                    xp INTEGER DEFAULT 0,
                    level_normal INTEGER DEFAULT 0,
                    level_fight INTEGER DEFAULT 0,
                    level_flying INTEGER DEFAULT 0,
                    level_poison INTEGER DEFAULT 0,
                    level_ground INTEGER DEFAULT 0,
                    level_rock INTEGER DEFAULT 0,
                    level_bug INTEGER DEFAULT 0,
                    level_ghost INTEGER DEFAULT 0,
                    level_steel INTEGER DEFAULT 0,
                    level_fire INTEGER DEFAULT 0,
                    level_water INTEGER DEFAULT 0,
                    level_grass INTEGER DEFAULT 0,
                    level_electric INTEGER DEFAULT 0,
                    level_psychic INTEGER DEFAULT 0,
                    level_ice INTEGER DEFAULT 0,
                    level_dragon INTEGER DEFAULT 0,
                    level_dark INTEGER DEFAULT 0
                )
            """
            cur.execute(cmd)
            await sql.commit()



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