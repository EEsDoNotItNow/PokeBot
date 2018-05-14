
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
        self.identifier=None
        self.generation_id=None
        self.type_id=None
        self.power=None
        self.pp_max=None
        self.accuracy=None
        self.priority=None
        self.target_id=None
        self.damage_class_id=None
        self.effect_id=None
        self.effect_chance=None
        self.contest_type_id=None
        self.contest_effect_id=None
        self.super_contest_effect_id=None

        self.short_effect=None
        self.effect=None


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
        cur = self.sql.cur
        data = cur.execute(cmd).fetchone()
        if data == None:
            raise ValueError(f"move_id {self.move_id} was not found in the db!")
        for key in data:
            if data[key] is not "" and hasattr(self,key):
                setattr(self,key,data[key])

        cmd = f"SELECT * FROM move_effect_prose WHERE effect_id={self.effect_id}"
        cur = self.sql.cur
        data = cur.execute(cmd).fetchone()
        for key in data:
            if data[key] is not "" and hasattr(self,key):
                setattr(self,key,data[key])




class MoveSlot(Move):

    def __init__(self, move_id, move_uuid=None, slot_number=None, pp=None, pp_max=None):
        """A move that currently sits in the slot of a pokemon

        @param move_id [REQUIRED] Id of the move, used to look up information in the DB
        @param move_uuid Unique ID of the move. If not given before being saved, will be generated
        @param slot_number Slot number (1-4) that a move sits in. Can be -1 to indicate it is temporary (When picking a new more, for instance)
        @param pp
        """

        super().__init__(move_id)

        self.move_uuid = move_uuid
        self.slot_number = slot_number
        self.pp = pp
        self.pp_max_slot = pp_max


    def __repr__(self):
        return f"MoveSlot({self.move_id}, {self.move_uuid})"


    def __str__(self):
        return f"{self.identifier} PP:{self.pp}/{self.pp_max}"


    async def em(self, debug=False):
        """Return an embed object to display this class
        """

        em = discord.Embed()
        em.title = self.identifier.title()
        em.add_field(name="Power", value=self.power)
        em.add_field(name="PP", value=f"{self.pp}/{self.pp_max}")
        if debug:
            em.add_field(name="Move UUID", value=self.move_uuid)
            em.add_field(name="Description", value=self.short_effect, inline=False)
            em.add_field(name="Accuracy", value=self.accuracy)
            em.add_field(name="Priority", value=self.priority)
            em.add_field(name="Move ID", value=self.move_id, inline=False)
        return em


    async def load(self):
        """Load data from DB on this move
        """

        await super().load()

        if self.move_uuid == None:
            # Generate a new UUID
            self.move_uuid = uuid.uuid4()
            self.pp = self.pp_max
        else:
            cmd = f"SELECT * FROM move_slots WHERE move_uuid={self.move_uuid}"
            cur = self.sql.cur
            data = cur.execute(cmd).fetchone()

            for key in data:
                if data[key] is not "" and hasattr(self,key):
                    setattr(self,key,data[key])