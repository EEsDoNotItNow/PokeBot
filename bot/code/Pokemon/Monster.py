

import discord
import numpy as np
import uuid

from ..Log import Log
from ..SQL import SQL

from .Pokemon import Pokemon
from . import EnumStatus



class Monster(Pokemon):


    def __init__(self, pokemon_id, monster_id=None):
        """Create a new Monster (an acutal pokemon in the sim)

        @param pokemon_id Id from the pokedex table, stats are based off this value
        @param monster_id if given, load all other values from the DB
        """
        self.log = Log()
        self.sql = SQL()

        # Init our superclass
        super().__init__(pokemon_id)

        self.monster_id = monster_id

        self.status = EnumStatus.ALIVE

        # Setup some sensible default values
        self.name = "NOT LOADED"

        self.hp_current = -1

        self.level = -1

        self.ability = None
        self.hidden_ability = None
        self.gender = "?"
        self.xp = 0

        self.iv_hp = 0
        self.iv_attack = 0
        self.iv_defense = 0
        self.iv_sp_attack = 0
        self.iv_sp_defense = 0
        self.iv_speed = 0

        self.ev_hp = 0
        self.ev_attack = 0
        self.ev_defense = 0
        self.ev_sp_attack = 0
        self.ev_sp_defense = 0
        self.ev_speed = 0

        self.hp = 0
        self.attack = 0
        self.defense = 0
        self.sp_attack = 0
        self.sp_defense = 0
        self.speed = 0


    def __repr__(self):
        return f"Monster({self.pokemon_id})"


    async def em(self, debug=False):
        """Return an embed object to display this class

        @param debug Display more stats!
        """

        em = discord.Embed()
        em.title = self.identifier.title()

        em.add_field(name="Level", value=self.level)


        if self.type2:
            type2 = f"/{str(self.type2).title()}"
        else:
            type2 = ""

        em.add_field(name="Type", value=f"{str(self.type1).title()}{type2}")


        stats_block = f"`HP: {self.hp_current}/{self.hp}`"
        stats_block += f"\n`ATK: {self.attack}`"
        stats_block += f"\n`DEF: {self.defense}`"
        stats_block += f"\n`S.ATK: {self.sp_attack}`"
        stats_block += f"\n`S.DEF: {self.sp_defense}`"
        stats_block += f"\n`SPD: {self.speed}`"

        em.add_field(name="Stats", value=stats_block, inline=False)

        em.add_field(name="Status", value=self.status)

        if debug:
            evs = {
                "ev_hp": self.ev_hp,
                "ev_attack": self.ev_attack,
                "ev_defense": self.ev_defense,
                "ev_sp_attack": self.ev_sp_attack,
                "ev_sp_defense": self.ev_sp_defense,
                "ev_speed": self.ev_speed,
            }
            em.add_field(name="EVs", value=evs)

            ivs = {
                "iv_hp": self.iv_hp,
                "iv_attack": self.iv_attack,
                "iv_defense": self.iv_defense,
                "iv_sp_attack": self.iv_sp_attack,
                "iv_sp_defense": self.iv_sp_defense,
                "iv_speed": self.iv_speed,
            }
            em.add_field(name="IVs", value=ivs)

        return em


    async def load(self):
        cur = self.sql.cur
        await super().load()

        self.name = self.identifier

        self.hp_current = self.base_hp

        self.level = await self.calc_level()

        if not self.monster_id:
            self.monster_id = str(uuid.uuid4())
            return

        cmd = "SELECT * FROM monsters WHERE pokemon_id=:pokemon_id AND monster_id=:monster_id"
        values = cur.execute(cmd, self.__dict__).fetchone()

        for key in values:
            setattr(self, key, values[key])


    async def save(self):

        cur = self.sql.cur
        cmd = """REPLACE INTO monsters
            (
                monster_id,
                pokemon_id,
                name,
                hp,
                attack,
                defense,
                sp_attack,
                sp_defense,
                speed,
                defense,
                xp,
                ability,
                hidden_ability,
                gender,
                iv_hp,
                iv_attack,
                iv_defense,
                iv_sp_attack,
                iv_sp_defense,
                iv_speed,
                ev_hp,
                ev_attack,
                ev_defense,
                ev_sp_attack,
                ev_sp_defense,
                ev_speed
            ) VALUES (
                :monster_id,
                :pokemon_id,
                :name,
                :hp,
                :attack,
                :defense,
                :sp_attack,
                :sp_defense,
                :speed,
                :defense,
                :xp,
                :ability,
                :hidden_ability,
                :gender,
                :iv_hp,
                :iv_attack,
                :iv_defense,
                :iv_sp_attack,
                :iv_sp_defense,
                :iv_speed,
                :ev_hp,
                :ev_attack,
                :ev_defense,
                :ev_sp_attack,
                :ev_sp_defense,
                :ev_speed
            )
        """
        # Build data table
        cur.execute(cmd, self.__dict__)
        await self.sql.commit(now=True)


    async def update_state(self):
        """Update state given current stats
        """
        self.level = await self.calc_level()
        self.attack = self._calc_stat(self.base_attack, self.iv_attack, self.ev_attack, self.level, 1)
        self.defense = self._calc_stat(self.base_defense, self.iv_defense, self.ev_defense, self.level, 1)
        self.sp_attack = self._calc_stat(self.base_sp_attack, self.iv_sp_attack, self.ev_sp_attack, self.level, 1)
        self.sp_defense = self._calc_stat(self.base_sp_defense, self.iv_sp_defense, self.ev_sp_defense, self.level, 1)
        self.speed = self._calc_stat(self.base_speed, self.iv_speed, self.ev_speed, self.level, 1)

        # HP must be handled with care!
        old_hp = self.hp
        self.hp = self._calc_hp(self.base_hp, self.iv_hp, self.ev_hp, self.level)
        await self.heal(amount=self.hp - old_hp)


    @staticmethod
    def _calc_stat(base, iv, ev, level, nature=1):
        return int(np.floor((np.floor(((2 * base + iv + np.floor(ev / 4)) * level) / 100) + 5) * nature))


    @staticmethod
    def _calc_hp(base, iv, ev, level):
        result = int(np.floor(((2 * base + iv + np.floor(ev / 4)) * level) / 100) + level + 10)
        return result


    async def calc_level(self):
        return int(np.floor(self.xp ** (1 / 3)))


    async def damage(self, amount, _type=None):
        """Add given amount of HP.

        @details Might set status to EnumStatus.DEAD if damage exceeds current hp!

        @param amount Amount to damage. Must be positive. Will not lower hp below zero.
        @param _type [OPTIONAL] Type of damage being dealt.
        """
        amount = int(amount)
        if amount <= 0:
            return

        self.hp_current -= amount

        if self.hp_current <= 0:
            # This will clear all 
            self.status = EnumStatus.DEAD
            self.hp_current = 0


    async def heal(self, amount=None):
        """Add given amount of HP.

        @param amount Amount to heal. If 'None', heal to full. Negative values are ignored, overflow is capped at max hp.
        """
        amount = int(amount)
        if amount > 0:
            if self.hp_current + amount > self.hp:
                self.hp_current = self.hp
            else:
                self.hp_current += amount
        elif amount <= 0:
            # Do nothing, you cannot heal by a negative amount!
            pass
        elif amount is None:
            self.hp_current = self.hp
