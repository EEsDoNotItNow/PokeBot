

import discord
import numpy as np

from ..Client import Client
from ..Log import Log
from ..SQL import SQL

from .Pokemon import Pokemon

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


    async def em(self, debug=False):
        """Return an embed object to display this class

        @param debug Display more stats!
        """

        em = discord.Embed()
        em.title = self.identifier.title()

        em.add_field(name="Level", value=self.level )


        if self.type2:
            type2 = f"/{str(self.type2).title()}"
        else:
            type2 = ""
        em.add_field(name="Type", value=f"{str(self.type1).title()}{type2}")

        hp = self.calc_stat( self.base_hp, self.iv_hp, self.ev_hp, self.level, 1  )

        stats_block = f"`HP: {self.hp}/{hp}`"
        stats_block += f"\n`ATK: {self.attack}`"
        stats_block += f"\n`DEF: {self.defense}`"
        stats_block += f"\n`S.ATK: {self.sp_attack}`"
        stats_block += f"\n`S.DEF: {self.sp_defense}`"
        stats_block += f"\n`SPD: {self.speed}`"

        em.add_field(name="Stats", value=stats_block, inline=False)

        if debug:
            evs = {      
                "ev_hp":self.ev_hp,
                "ev_attack":self.ev_attack,
                "ev_defense":self.ev_defense,
                "ev_sp_attack":self.ev_sp_attack,
                "ev_sp_defense":self.ev_sp_defense,
                "ev_speed":self.ev_speed,
            }
            em.add_field(name="EVs", value=evs)

            ivs = {      
                "iv_hp":self.iv_hp,
                "iv_attack":self.iv_attack,
                "iv_defense":self.iv_defense,
                "iv_sp_attack":self.iv_sp_attack,
                "iv_sp_defense":self.iv_sp_defense,
                "iv_speed":self.iv_speed,
            }
            em.add_field(name="IVs", value=ivs)

        return em


    @staticmethod
    def calc_stat(base, iv, ev, level, nature=1):
        return  int(np.floor( ( np.floor( ( ( 2*base + iv + np.floor(ev/4) )*level)/100 ) + 5 )*nature))


    @staticmethod
    def calc_hp(base, iv, ev, level):
        result = int(np.floor( ( ( 2 * base + iv + np.floor(ev/4))*level )/100 ) + level + 10)
        return result


    async def calc_level(self):
        return int(np.floor( self.xp**(1/3) ))
    

    async def load(self):
        await super().load()

        self.hp_current = self.base_hp
        self.xp = 0

        self.level = await self.calc_level()

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

        if self.monster_id:
            # TODO: Load from SQL
            raise NotImplementedError()

        # TODO: We also need to load from the SQL 


    async def update_state(self):
        """Update state given current stats
        """

        self.level = await self.calc_level()
        self.hp = self.calc_stat(self.base_hp, self.iv_hp, self.ev_hp, self.level, 1)
        self.attack = self.calc_stat(self.base_attack, self.iv_attack, self.ev_attack, self.level, 1)
        self.defense = self.calc_stat(self.base_defense, self.iv_defense, self.ev_defense, self.level, 1)
        self.sp_attack = self.calc_stat(self.base_sp_attack, self.iv_sp_attack, self.ev_sp_attack, self.level, 1)
        self.sp_defense = self.calc_stat(self.base_sp_defense, self.iv_sp_defense, self.ev_sp_defense, self.level, 1)
        self.speed = self.calc_stat(self.base_speed, self.iv_speed, self.ev_speed, self.level, 1)