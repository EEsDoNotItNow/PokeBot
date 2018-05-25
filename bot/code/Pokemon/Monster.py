

import discord
import numpy as np
import uuid

from ..Log import Log
from ..SQL import SQL
from ..Client import EmojiMap

from .Pokemon import Pokemon
from .Move import MoveSlot
from . import EnumStatus



class Monster(Pokemon):


    def __init__(self, monster_id=None, pokemon_id=None):
        """Create a new Monster (an actual pokemon in the sim)

        @param pokemon_id Id from the pokedex table, stats are based off this value
        @param monster_id if given, load all other values from the DB
        """
        self.log = Log()
        self.sql = SQL()

        # Init our superclass
        if pokemon_id:
            super().__init__(pokemon_id)

        self.loaded = False

        self.monster_id = monster_id

        self.status = EnumStatus.ALIVE

        self.move_slots = [None, None, None, None]

        # Setup some sensible default values
        self.name = None

        self.hp_current = -1

        self.level = -1

        self.ability = None
        self.hidden_ability = None
        self.gender = None
        self.xp = 0

        # "Genetics" of the pokemon
        self.iv_hp = 0
        self.iv_attack = 0
        self.iv_defense = 0
        self.iv_sp_attack = 0
        self.iv_sp_defense = 0
        self.iv_speed = 0

        # Effort values, come from winning battles
        self.ev_hp = 0
        self.ev_attack = 0
        self.ev_defense = 0
        self.ev_sp_attack = 0
        self.ev_sp_defense = 0
        self.ev_speed = 0

        # Resultant stat values
        self.hp = 0
        self.attack = 0
        self.defense = 0
        self.sp_attack = 0
        self.sp_defense = 0
        self.speed = 0

        # Stage of stats in battles (-7 <= x <= 6)
        self.stage_hp = 0
        self.stage_attack = 0
        self.stage_defense = 0
        self.stage_sp_attack = 0
        self.stage_sp_defense = 0
        self.stage_speed = 0


    def __repr__(self):
        return f"Monster({self.monster_id})"


    def __eq__(self, other):
        if type(other) is Monster:
            return self.monster_id == other.monster_id and self.pokemon_id == other.pokemon_id
        if type(other) is Pokemon:
            return self.pokemon_id == other.pokemon_id
        raise NotImplementedError


    def __ne__(self, other):
        return not self.__eq__(other)


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


    async def text_card(self, bar_length=20, debug=False, opponent=False):
        """Return a text card
        """
        msg = "```\n"

        # Handle Top Bar
        ng_tag = f"{self.name}{self.gender}"
        lv_tag = f"Lv{self.level}"
        msg += f"{ng_tag:13} {lv_tag:5}"

        # Handle HP bar
        hp_ratio = self.hp_current / self.hp

        hp_blocks_full = int(bar_length * hp_ratio)
        hp_blocks_empty = bar_length - hp_blocks_full

        msg += f"\nHP:[{'#' * hp_blocks_full}{' ' * hp_blocks_empty}]"
        if not opponent:
            msg += f" {self.hp_current}/{self.hp}"

        # Handle XP bar
        if not opponent:
            if self.level == 100:
                xp_ratio = 1.0
            else:
                xp_base = await self.calc_xp_for_level(self.level)
                xp_next = await self.calc_xp_for_level(self.level + 1)
                xp_ratio = (self.xp - xp_base) / (xp_next - xp_base)

            xp_blocks_full = int(bar_length * xp_ratio)
            xp_blocks_empty = bar_length - xp_blocks_full
            msg += f"\nXP:[{'#' * xp_blocks_full}{' ' * xp_blocks_empty}]"

            msg += "\nMoves:"
            for move in self.move_slots:
                msg += f"\n   {move}"

        if debug:
            msg += "\n"
            evs = {
                "ev_hp": self.ev_hp,
                "ev_attack": self.ev_attack,
                "ev_defense": self.ev_defense,
                "ev_sp_attack": self.ev_sp_attack,
                "ev_sp_defense": self.ev_sp_defense,
                "ev_speed": self.ev_speed,
            }
            ivs = {
                "iv_hp": self.iv_hp,
                "iv_attack": self.iv_attack,
                "iv_defense": self.iv_defense,
                "iv_sp_attack": self.iv_sp_attack,
                "iv_sp_defense": self.iv_sp_defense,
                "iv_speed": self.iv_speed,
            }
            msg += f"{evs}\n{ivs}"

        msg += "```"
        return msg


    async def load(self):
        cur = self.sql.cur

        if self.monster_id is not None:
            cmd = "SELECT * FROM monsters WHERE monster_id=:monster_id"
            values = cur.execute(cmd, self.__dict__).fetchone()
            for key in values:
                setattr(self, key, values[key])
        else:
            self.monster_id = str(uuid.uuid4())

        super().__init__(pokemon_id=self.pokemon_id)
        await super().load()

        await self.update_state()
        self.loaded = True


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


    async def spawn(self, level=5, fast=False):
        # We MUST have loaded before we can do anything!
        if not self.loaded:
            await self.load()

        self.name = self.identifier.title()

        em = EmojiMap()
        male = em(":male:")
        female = em(":female:")

        if self.gender_rate == -1:
            self.gender = ''
        else:
            if self.gender_rate == 0:
                m_ratio = 1
                f_ratio = 0
            elif self.gender_rate == 1:
                m_ratio = 7 / 8
                f_ratio = 1 - m_ratio
            elif self.gender_rate == 2:
                m_ratio = 3 / 4
                f_ratio = 1 - m_ratio
            elif self.gender_rate == 4:
                m_ratio = 1 / 2
                f_ratio = 1 - m_ratio
            elif self.gender_rate == 6:
                m_ratio = 1 / 4
                f_ratio = 1 - m_ratio
            elif self.gender_rate == 7:
                m_ratio = 1 / 8
                f_ratio = 1 - m_ratio
            elif self.gender_rate == 8:
                m_ratio = 0
                f_ratio = 1
            self.gender = np.random.choice((male, female), p=(m_ratio, f_ratio))

        self.xp = await self.calc_xp_for_level(level)

        self.iv_hp = np.random.randint(0, 31)
        self.iv_attack = np.random.randint(0, 31)
        self.iv_defense = np.random.randint(0, 31)
        self.iv_sp_attack = np.random.randint(0, 31)
        self.iv_sp_defense = np.random.randint(0, 31)
        self.iv_speed = np.random.randint(0, 31)

        await self.update_state()

        self.hp_current = self.hp

        # All slow operations happen after this gate
        if fast:
            return

        # Pick moves
        cmd = f"""
            SELECT move_id
            FROM pokemon_moves
            WHERE pokemon_id={self.pokemon_id}
                AND version_group_id=18
                AND pokemon_move_method_id=1
                AND level<={self.level}
            ORDER BY level DESC"""
        cur = self.sql.cur
        data = cur.execute(cmd).fetchall()
        for idx, move_id in enumerate(data[:4]):
            self.log.info(move_id)
            cmd = f"""
                SELECT *
                FROM moves
                WHERE move_id=:move_id"""
            move_data = cur.execute(cmd, move_id).fetchone()
            self.log.info(move_data)
            self.move_slots[idx] = MoveSlot(move_data['move_id'], slot_number=idx)
            await self.move_slots[idx].load()



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
        # 'SELECT * FROM experience_lookup WHERE growth_rate_id=1 AND experience<=9 ORDER BY level DESC LIMIT 1'
        cmd = """SELECT * FROM experience_lookup
                 WHERE growth_rate_id=:growth_rate_id AND experience<=:xp
                 ORDER BY level
                 DESC LIMIT 1"""
        result = self.sql.cur.execute(cmd, self.__dict__).fetchone()
        if result is None:
            self.log.error("Failed a lookup on the following:")
            self.log.error(f"Pokemon ID: {self.pokemon_id}")
            self.log.error(f"growth_rate_id: {self.growth_rate_id}")
            self.log.error(f"xp: {self.xp}")
            raise RuntimeError()

        return int(result['level'])
        # return int(np.floor(self.xp ** (1 / 3)))


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

        @param amount Amount to heal. If 'None', heal to full.
            Negative values are ignored, overflow is capped at max hp.
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


    async def capture(self, trainer_id):
        """Capture a pokemon. This will register it to the player, and attempt to find a place it the party for it.

        @param trainer_id Trainer that captured this poke.
        """
        raise NotImplementedError()


    async def level_up(self):
        """If a Pokemon has experenced a level up, handle this.

        @param trainer_id Trainer that captured this poke.
        """
        while self.level != await self.calc_level():
            # Check for evolution conditions
            #   Level based evolve?
            #   Other conditional evolution?
            #   Prompt trainer to stop or allow evolution (30 second timeout)

            # Check for new moves
            #   Pormpt user to learn it if needed

            await self.update_state()
            await self.save()
