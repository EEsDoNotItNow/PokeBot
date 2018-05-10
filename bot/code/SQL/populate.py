
import json
import time

from pprint import pprint

from ..Log import Log
from . import SQL

async def populate():
    """Attmept to populate basic tables
    """

    log = Log()
    sql = SQL.SQL()

    log.info("Loading pokedex data")

    with open("data/base.json") as fp:
        data = json.load(fp)

    log.info(f"Must load {len(data)} rows")
    cur = sql.cur
    for key in data['pokedex']:
        # log.info(data[key])
        cmd = """INSERT INTO pokedex 
        (
            pokemon_id,
            identifier,
            height,
            weight,
            base_xp,
            base_hp,
            base_attack,
            base_defense,
            base_sp_attack,
            base_sp_defense,
            base_speed,
            effort_hp,
            effort_attack,
            effort_defense,
            effort_sp_attack,
            effort_sp_defense,
            effort_speed,
            gender_ratio,
            catch_rate,
            hatch_time,
            type1,
            type2
        ) VALUES (
            :pokemon_id,
            :identifier,
            :height,
            :weight,
            :base_xp,
            :base_hp,
            :base_attack,
            :base_defense,
            :base_sp_attack,
            :base_sp_defense,
            :base_speed,
            :effort_hp,
            :effort_attack,
            :effort_defense,
            :effort_sp_attack,
            :effort_sp_defense,
            :effort_speed,
            :gender_ratio,
            :catch_rate,
            :hatch_time,
            :type1,
            :type2
        )"""
        try:
            cur.execute(cmd, data['pokedex'][key])
        except:
            # log.exception(data[key])
            pprint(data['pokedex']["1"])
            pprint(data['pokedex'][key])
            raise
    await sql.commit()
    log.info("Writes completed")

    """
                (
                pokemon_id TEXT DEFAULT 0,
                identifier TEXT NOT NULL,
                height INTEGER NOT NULL,
                weight INTEGER NOT NULL,
                base_xp INTEGER NOT NULL,
                base_hp INTEGER NOT NULL,
                base_attack INTEGER NOT NULL, 
                base_defense INTEGER NOT NULL, 
                base_sp_attack INTEGER NOT NULL,
                base_sp_defense INTEGER NOT NULL,
                base_speed INTEGER NOT NULL,
                effort_hp INTEGER NOT NULL,
                effort_attack INTEGER NOT NULL, 
                effort_defense INTEGER NOT NULL, 
                effort_sp_attack INTEGER NOT NULL,
                effort_sp_defense INTEGER NOT NULL,
                effort_speed INTEGER NOT NULL,
                gender_ratio INTEGER NOT NULL,
                catch_rate INTEGER,
                hatch_time INTEGER,
                abilities TEXT,
                hidden_abilities TEXT
            )
    """
