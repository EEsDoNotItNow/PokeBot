
from ..Log import Log
from . import SQL

async def table_setup():
    """Setup any SQL tables needed for this class
    """
    log = Log()
    log.info("Check to see if trainers exists.")
    sql = SQL.SQL()
    if not await sql.table_exists("trainers"):
        log.info("Create trainers table")
        cur = sql.cur
        cmd = """
            CREATE TABLE trainers 
            (
                trainer_id TEXT NOT NULL,
                user_id TEXT NOT NULL, 
                server_id TEXT NOT NULL,
                nickname TEXT,
                created_on TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """
        cur.execute(cmd)
        await sql.commit()


    log.info("Check to see if trainer_stats exists.")
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
