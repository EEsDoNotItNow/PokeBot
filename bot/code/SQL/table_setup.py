
from ..Log import Log
from . import SQL

async def table_setup():
    """Setup any SQL tables needed for this class
    """
    log = Log()
    sql = SQL.SQL()
    
    log.info("Check to see if users exists.")
    if not await sql.table_exists("users"):
        log.info("Create users table")
        cur = sql.cur
        cmd = """    
            CREATE TABLE IF NOT EXISTS users
            (
                name TEXT NOT NULL,
                user_id TEXT NOT NULL,
                discriminator TEXT,
                avatar TEXT,
                bot BOOLEAN,
                avatar_url TEXT,
                default_avatar TEXT,
                default_avatar_url TEXT,
                mention TEXT,
                created_at INTEGER
            )"""
        cur.execute(cmd)
        await sql.commit()


    log.info("Check to see if trainers exists.")
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
                trainer_id TEXT NOT NULL UNIQUE,
                pokecoin REAL DEFAULT 100,
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


    log.info("Check to see if trainer_pokedex exists.")
    if not await sql.table_exists("trainer_pokedex"):
        log.info("Create trainer_pokedex table")
        cur = sql.cur
        cmd = """
            CREATE TABLE trainer_pokedex
            (
                trainer_id TEXT NOT NULL,
                pokemon_id TEXT NOT NULL,
                caught INTEGER DEFAULT 0,
                seen INTEGER DEFAULT 0,
                defeated INTEGER DEFAULT 0
            )
        """
        cur.execute(cmd)
        await sql.commit()


    log.info("Check to see if pokedex exists.")
    if not await sql.table_exists("pokedex"):
        log.info("Create pokedex table")
        cur = sql.cur
        cmd = """
            CREATE TABLE pokedex
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
                gendered BOOLEAN DEFAULT 1,
                gender_ratio REAL DEFAULT 0.5,
                catch_rate INTEGER NOT NULL,
                hatch_time_min INTEGER,
                hatch_time_max INTEGER,
                abilities TEXT,
                hidden_abilities TEXT
            )
        """
        cur.execute(cmd)
        await sql.commit()


    log.info("Check to see if monsters exists.")
    if not await sql.table_exists("monsters"):
        log.info("Create monsters table")
        cur = sql.cur
        cmd = """
            CREATE TABLE monsters
            (
                pokemon_id TEXT NOT NULL,
                monster_id TEXT NOT NULL,
                name TEXT,
                hp INTEGER NOT NULL,
                xp INTEGER NOT NULL,
                ability TEXT, 
                hidden_ability TEXT,
                gender TEXT,
                iv_hp INTEGER DEFAULT 0,
                iv_attack INTEGER DEFAULT 0,
                iv_defense INTEGER DEFAULT 0,
                iv_sp_attack INTEGER DEFAULT 0,
                iv_sp_defense INTEGER DEFAULT 0,
                iv_speed INTEGER DEFAULT 0,
                ev_hp INTEGER DEFAULT 0,
                ev_attack INTEGER DEFAULT 0,
                ev_defense INTEGER DEFAULT 0,
                ev_sp_attack INTEGER DEFAULT 0,
                ev_sp_defense INTEGER DEFAULT 0,
                ev_speed INTEGER DEFAULT 0
            )
        """
        cur.execute(cmd)
        await sql.commit()