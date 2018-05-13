
from pprint import pprint
import csv
import json
import time
import pathlib

from ..Log import Log
from . import SQL


async def ingest_csv(csv_dir):
    log = Log()
    dex = {}

    log.info("Load pokemon.csv")
    t_step = time.time()
    with open(csv_dir / "pokemon/pokemon.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        raw_dex = []
        for entry in reader:
            raw_dex.append(dict(entry))
            for key in raw_dex[-1]:
                try:
                    raw_dex[-1][key] = int(raw_dex[-1][key])
                except ValueError:
                    pass

    # We are unable to guarentee that ALL entries will have all data, 
    #   so we load them with default NULLs into the DB
    for entry in raw_dex:
        pokemon_id = entry['id']
        dex[pokemon_id] = {}
        dex[pokemon_id]['gender_ratio'] = None
        dex[pokemon_id]['catch_rate'] = None
        dex[pokemon_id]['hatch_time'] = None
        dex[pokemon_id]['base_happiness'] = None
        dex[pokemon_id]['type2'] = None


    for entry in raw_dex:
        pokemon_id = entry['id']
        dex[pokemon_id]['pokemon_id'] = pokemon_id
        dex[pokemon_id]['identifier'] = entry['identifier']
        dex[pokemon_id]['height'] = entry['height']
        dex[pokemon_id]['weight'] = entry['weight']
        dex[pokemon_id]['base_xp'] = entry['base_experience']
    log.info(f"pokemon loaded in {time.time()-t_step:.3f}s")


    log.info("Load pokemon_stats.csv")
    t_step = time.time()
    with open(csv_dir / "pokemon/pokemon_stats.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        raw_stats = []
        for entry in reader:
            raw_stats.append(dict(entry))
            for key in raw_stats[-1]:
                try:
                    raw_stats[-1][key] = int(raw_stats[-1][key])
                except ValueError:
                    pass

    stat_lookup = { 1:"hp", 2:"attack", 3:"defense", 4:"sp_attack", 5:"sp_defense", 6:"speed"}
    for entry in raw_stats:
        pokemon_id = entry['pokemon_id']
        base_key = "base_" + stat_lookup[entry['stat_id']]
        effort_key = "effort_" + stat_lookup[entry['stat_id']]
        dex[pokemon_id][base_key] = entry['base_stat']
        dex[pokemon_id][effort_key] = entry['effort']
    log.info(f"pokemon_stats loaded in {time.time()-t_step:.3f}s")


    log.info("Load pokemon_species.csv")
    t_step = time.time()
    with open(csv_dir / "pokemon/pokemon_species.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        species_stats = []
        for entry in reader:
            species_stats.append(dict(entry))
            for key in species_stats[-1]:
                try:
                    species_stats[-1][key] = int(species_stats[-1][key])
                except ValueError:
                    pass

    for entry in species_stats:
        pokemon_id = entry['id']
        dex[pokemon_id]['gender_ratio'] = entry['gender_rate']
        dex[pokemon_id]['catch_rate'] = entry['capture_rate']
        dex[pokemon_id]['hatch_time'] = entry['hatch_counter']
        dex[pokemon_id]['base_happiness'] = entry['base_happiness']
    log.info(f"pokemon_species loaded in {time.time()-t_step:.3f}s")


    log.info("Load pokemon_moves.csv")
    t_step = time.time()
    with open(csv_dir / "pokemon/pokemon_moves.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        pokemon_moves = []
        for entry in reader:
            pokemon_moves.append(dict(entry))
            for key in pokemon_moves[-1]:
                try:
                    pokemon_moves[-1][key] = int(pokemon_moves[-1][key])
                except ValueError:
                    pass
    log.info(f"pokemon_moves loaded in {time.time()-t_step:.3f}s")


    # Handle Pokemon
    log.info("Load types.csv")
    t_step = time.time()
    with open(csv_dir / "pokemon/types.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        types_lookup = []
        for entry in reader:
            types_lookup.append(dict(entry))
            for key in types_lookup[-1]:
                try:
                    types_lookup[-1][key] = int(types_lookup[-1][key])
                except ValueError:
                    pass
    temp = tuple(types_lookup)
    types_lookup = {}
    for entry in temp:
        types_lookup[entry['id']] = entry['identifier']
    log.info(f"types loaded in {time.time()-t_step:.3f}s")


    log.info("Load pokemon_types.csv")
    t_step = time.time()
    with open(csv_dir / "pokemon/pokemon_types.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        pokemon_types = []
        for entry in reader:
            pokemon_types.append(dict(entry))
            for key in pokemon_types[-1]:
                try:
                    pokemon_types[-1][key] = int(pokemon_types[-1][key])
                except ValueError:
                    pass

    for entry in pokemon_types:
        pokemon_id = entry['pokemon_id']
        if entry['slot'] == 1:
            dex[pokemon_id]['type1'] = entry['type_id']
        elif entry['slot'] == 2:
            dex[pokemon_id]['type2'] = entry['type_id']
        else:
            raise KeyError(f"Unknown slot '{entry['slot']}'")
    log.info(f"pokemon_types loaded in {time.time()-t_step:.3f}s")


    log.info("Load type_efficacy.csv")
    t_step = time.time()
    with open(csv_dir / "pokemon/type_efficacy.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        type_efficacy = []
        for entry in reader:
            type_efficacy.append(dict(entry))
            for key in type_efficacy[-1]:
                try:
                    type_efficacy[-1][key] = int(type_efficacy[-1][key])
                except ValueError:
                    pass
    log.info(f"type_efficacy loaded in {time.time()-t_step:.3f}s")

    # Handle world generation

    log.info("Load encounters.csv")
    t_step = time.time()
    with open(csv_dir / "world/encounters.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        encounters = []
        for entry in reader:
            encounters.append(dict(entry))
            for key in encounters[-1]:
                try:
                    encounters[-1][key] = int(encounters[-1][key])
                except ValueError:
                    pass
    log.info(f"encounters loaded in {time.time()-t_step:.3f}s")

    log.info("Load location_names.csv")
    t_step = time.time()
    with open(csv_dir / "world/location_names.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        location_names = []
        for entry in reader:
            if entry['local_language_id'] != '9':
                continue
            location_names.append(dict(entry))
            for key in location_names[-1]:
                try:
                    location_names[-1][key] = int(location_names[-1][key])
                except ValueError:
                    pass
    log.info(f"location_names loaded in {time.time()-t_step:.3f}s")

    log.info("Load zone_connections.csv")
    t_step = time.time()
    with open(csv_dir / "world/zone_connections.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        zone_connections = []
        for entry in reader:
            zone_connections.append(dict(entry))
            for key in zone_connections[-1]:
                try:
                    zone_connections[-1][key] = int(zone_connections[-1][key])
                except ValueError:
                    pass
    log.info(f"zone_connections loaded in {time.time()-t_step:.3f}s")

    locations = []

    output = {}
    output['encounters'] = encounters
    output['location_names'] = location_names
    output['pokedex'] = dex
    output['pokemon_moves'] = pokemon_moves
    output['type_efficacy'] = type_efficacy
    output['types'] = types_lookup
    output['zone_connections'] = zone_connections

    return output

async def populate():
    """Attmept to populate basic tables
    """

    log = Log()
    sql = SQL.SQL()

    log.info("Loading pokedex data")

    csv_dir = pathlib.Path("data/")
    t_start_csv = time.time()
    data = await ingest_csv(csv_dir)

    log.info(f"Full csv load took {time.time()-t_start_csv:.3f}s")

    log.info(f"Must load {len(data['pokedex'])} pokedex rows")
    t_start_sql = time.time()
    t_step = time.time()
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
    log.info(f"pokedex loaded in {time.time()-t_step:.3f}s")

    log.info(f"Must load types {len(data['types']):,d} rows")
    t_step = time.time()
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
    log.info(f"types loaded in {time.time()-t_step:.3f}s")

    log.info(f"Must load type_efficacy {len(data['type_efficacy']):,d} rows")
    t_step = time.time()
    cur = sql.cur
    for entry in data['type_efficacy']:
        # log.info(data[key])
        cmd = """INSERT INTO type_efficacy 
        (
            damage_type_id,
            target_type_id,
            damage_factor
        ) VALUES (
            :damage_type_id,
            :target_type_id,
            :damage_factor
        )"""
        try:
            cur.execute(cmd, entry)
        except:
            log.critical("Loading of data failed, we cannot conintue!")
            raise
    log.info(f"type_efficacy loaded in {time.time()-t_step:.3f}s")



    log.info(f"Must load encounters {len(data['encounters']):,d} rows")
    t_step = time.time()
    cur = sql.cur
    for entry in data['encounters']:
        # log.info(data[key])
        entry['location_id'] = entry['id']
        cmd = """INSERT INTO encounters 
        (
            location_id,
            encounter_slot_id,
            location_area_id,
            max_level,
            min_level,
            pokemon_id,
            version_id
        ) VALUES (
            :location_id,
            :encounter_slot_id,
            :location_area_id,
            :max_level,
            :min_level,
            :pokemon_id,
            :version_id
        )"""
        try:
            cur.execute(cmd, entry)
        except:
            log.critical("Loading of data failed, we cannot conintue!")
            print(entry)
            raise
    log.info(f"encounters loaded in {time.time()-t_step:.3f}s")


    log.info(f"Must load locations {len(data['location_names']):,d} rows")
    t_step = time.time()
    cur = sql.cur
    for entry in data['location_names']:
        # log.info(data[key])
        cmd = """INSERT INTO locations 
        (
            location_id,
            name
        ) VALUES (
            :location_id,
            :name
        )"""
        try:
            cur.execute(cmd, entry)
        except:
            log.critical("Loading of data failed, we cannot conintue!")
            raise
    log.info(f"location_names loaded in {time.time()-t_step:.3f}s")


    log.info(f"Must load zone_connections {len(data['zone_connections']):,d} rows")
    t_step = time.time()
    cur = sql.cur
    for entry in data['zone_connections']:
        # log.info(data[key])
        cmd = """INSERT INTO zone_connections 
        (
            location_id_1,
            location_id_2,
            distance
        ) VALUES (
            :location_id_1,
            :location_id_2,
            :distance
        )"""
        try:
            cur.execute(cmd, entry)
        except:
            log.critical("Loading of data failed, we cannot conintue!")
            raise
    log.info(f"zone_connections loaded in {time.time()-t_step:.3f}s")


    log.info(f"SQL Population took {time.time()-t_start_sql:.3f}s")
    log.info(f"Total Population took {time.time()-t_start_csv:.3f}s")


    await sql.commit()

    log.info("Populate wites completed")



