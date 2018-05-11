
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

    log.info(f"Must load {len(data['pokedex'])} rows")
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
            log.critical("Loading of data failed, we cannot conintue!")
            raise

    log.info(f"Must load {len(data['types'])} rows")
    cur = sql.cur
    for key in data['types']:
        cmd = """INSERT INTO types 
        (
            type_id,
            identifier
        ) VALUES (
            :type_id,
            :identifier
        )"""
        type_id = key
        identifier = data['types'][key]
        try:
            cur.execute(cmd, locals())
        except:
            log.critical(type_id)
            log.critical(identifier)
            log.critical("Loading of data failed, we cannot conintue!")
            raise

    await sql.commit()

    log.info("Populate wites completed")
