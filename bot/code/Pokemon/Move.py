
import discord
import uuid

from ..Log import Log
from ..SQL import SQL


class Move:

    def __init__(self, move_id):
        self.sql = SQL()
        self.log = Log()
        self.move_id = move_id

        # Init simple placeholder values
        self.identifier = None
        self.generation_id = None
        self.type_id = None
        self.power = None
        self.pp_max = None
        self.accuracy = None
        self.priority = None
        self.target_id = None
        self.damage_class_id = None
        self.effect_id = None
        self.effect_chance = None
        self.contest_type_id = None
        self.contest_effect_id = None
        self.super_contest_effect_id = None

        self.short_effect = None
        self.effect = None

        self.move_loaded = False


    def __repr__(self):
        return f"Move({self.move_id})"


    def __str__(self):
        return f"Move<{self.identifier}>"


    async def em(self, debug=False):
        """Return an embed object to display this class
        """

        em = discord.Embed()
        em.title = self.identifier.title()
        em.add_field(name="Power", value=self.power)
        em.add_field(name="PP", value=self.pp_max)
        em.add_field(name="Description", value=self.short_effect, inline=False)
        em.add_field(name="Accuracy", value=self.accuracy)
        em.add_field(name="Priority", value=self.priority)
        if debug:
            em.add_field(name="Move ID", value=self.move_id, inline=False)
        return em

    async def load(self):
        """Load data from DB on this move
        """
        cmd = f"SELECT * FROM moves WHERE move_id={self.move_id}"
        self.log.info(cmd)
        cur = self.sql.cur
        data = cur.execute(cmd).fetchone()
        if data is None:
            raise ValueError(f"move_id {self.move_id} was not found in the db!")
        for key in data:
            setattr(self, key, data[key])

        cmd = f"SELECT * FROM move_effect_prose WHERE effect_id={self.effect_id}"
        cur = self.sql.cur
        data = cur.execute(cmd).fetchone()
        for key in data:
            setattr(self, key, data[key])

        self.move_loaded = True



class MoveSlot(Move):

    def __init__(self, move_id=None, monster_id=None, move_slot_uuid=None, slot_number=None):
        """A move that currently sits in the slot of a pokemon

        @param move_id [REQUIRED] Id of the move, used to look up information in the DB
        @param move_slot_uuid Unique ID of the move. If not given before being saved, will be generated
        @param monster_id Unique ID of the monster this move is affixed to
        """

        if move_id is not None:
            super().__init__(move_id)
        else:
            self.sql = SQL()
            self.log = Log()
            self.move_id = None

        self.move_slot_uuid = move_slot_uuid
        self.monster_id = monster_id
        self.slot_number = slot_number
        self.pp = None
        self.pp_max_slot = None

        self.move_slot_loaded = False


    def __repr__(self):
        return f"MoveSlot({self.move_id}, {self.move_slot_uuid})"


    def __str__(self):
        return f"{self.identifier} PP:{self.pp}/{self.pp_max_slot}"


    async def em(self, debug=False):
        """Return an embed object to display this class
        """

        em = discord.Embed()
        em.title = self.identifier.title()
        em.add_field(name="Power", value=self.power)
        em.add_field(name="PP", value=f"{self.pp}/{self.pp_max_slot}")
        if debug:
            em.add_field(name="Move UUID", value=self.move_slot_uuid)
            em.add_field(name="Description", value=self.short_effect, inline=False)
            em.add_field(name="Accuracy", value=self.accuracy)
            em.add_field(name="Priority", value=self.priority)
            em.add_field(name="Move ID", value=self.move_id, inline=False)
        return em


    async def load(self):
        """Load data from DB on this move
        """

        if self.move_slot_uuid is None:
            # Assume we were given a move_id and load!
            await super().load()

            # Generate a new UUID
            self.move_slot_uuid = str(uuid.uuid4())
            self.pp = self.pp_max
            self.pp_max_slot = self.pp_max
        else:
            cmd = f"SELECT * FROM move_slots WHERE move_slot_uuid=:move_slot_uuid"
            cur = self.sql.cur
            data = cur.execute(cmd, self.__dict__).fetchone()

            for key in data:
                setattr(self, key, data[key])
            # We don't know our move_id until we have loaded from the SQL DB, load that info now
            self.log.info(self.__dict__)
            await super().load()
        self.move_slot_loaded = True



    async def save(self):
        """Load data from DB on this move
        """
        cur = self.sql.cur
        cmd = """
            INSERT OR REPLACE
            INTO move_slots
            (
                move_id,
                move_slot_uuid,
                monster_id,
                slot_number,
                pp,
                pp_max_slot
            ) VALUES (
                :move_id,
                :move_slot_uuid,
                :monster_id,
                :slot_number,
                :pp,
                :pp_max_slot
            )
        """
        cur.execute(cmd, self.__dict__)
        await self.sql.commit(now=True)
