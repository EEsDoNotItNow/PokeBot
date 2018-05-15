

import discord
import datetime
import dateutil.parser
import uuid
import numpy

from ..Client import Client
from ..Log import Log
from ..SQL import SQL


class Trainer:

    def __init__(self, trainer_id=None, user_id=None, server_id=None):
        self.client = Client()
        self.log = Log()
        self.sql = SQL()

        self.trainer_id = trainer_id

        self.user_id = user_id 
        self.server_id = server_id

        self.is_zombie = False


    async def load(self, create_ok=False):
        """Given known state, attmpt to load. If unable to find trainer, create one!
        """

        cmd = "SELECT * FROM trainers WHERE trainer_id = :trainer_id"
        values = self.sql.cur.execute(cmd, self.__dict__).fetchone()

        if values is None:
            if create_ok:
                await self.create()
                cmd = "SELECT * FROM trainers WHERE user_id=:user_id AND server_id=:server_id"
                values = self.sql.cur.execute(cmd, self.__dict__).fetchone()
            else:
                # We don't exist yet?! AHHHH! 
                raise ValueError("Attempted to load Trainer that doesn't exist yet")

        self.created_on = dateutil.parser.parse(values['created_on'])
        self.nickname = values['nickname']
        self.server_id = values['server_id']
        self.trainer_id = values['trainer_id']
        self.user_id = values['user_id']

        cmd = f"SELECT * FROM trainer_stats WHERE trainer_id=:trainer_id"
        self.log.info(cmd)
        values = self.sql.cur.execute(cmd, self.__dict__).fetchone()

        self.stats = dict(values)


    async def create(self):
        """Create self, and all basic tables needed to exist
        """
        cur = self.sql.cur

        user = Client().get_server(self.server_id).get_member(self.user_id)

        self.nickname = user.nick if user.nick else user.name

        nickname = self.nickname
        trainer_id = str(uuid.uuid4())
        now = datetime.datetime.now()
        user_id = self.user_id
        server_id = self.server_id

        self.log.critical(locals())

        cmd = """INSERT INTO trainers
            (trainer_id,
            user_id,
            server_id,
            nickname,
            created_on)
            VALUES
            (:trainer_id, :user_id, :server_id, :nickname, :now)"""
        cur.execute(cmd, locals())

        cmd = """INSERT INTO trainer_stats
        (trainer_id)
        VALUES
        (:trainer_id)"""
        cur.execute(cmd, locals())

        cmd = """INSERT INTO trainer_data
        (trainer_id)
        VALUES
        (:trainer_id)"""
        cur.execute(cmd, locals())

        cmd = """INSERT INTO trainer_party
        (trainer_id)
        VALUES
        (:trainer_id)"""
        cur.execute(cmd, locals())

        await self.sql.commit(now=True)
        self.log.info(f"New trainer has been born! Welcome {trainer_id}")


    def __eq__(self, other):
        if type(other) != Trainer:
            raise NotImplimentedError()

        return str(self.trainer_id) == str(other.trainer_id)


    def __ne__(self, other):
        if type(other) != Trainer:
            raise NotImplimentedError()
        
        return str(self.trainer_id) != str(other.trainer_id)


    async def log_stats(self, stats_dict):
        """Merge the stats_dict with the SQL DB entry, adding where able

        @raises ValueError when stats_dict contains an invalid key
        """

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
