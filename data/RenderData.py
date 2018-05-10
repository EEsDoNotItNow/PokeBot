#!/usr/bin/env python3

import csv
import json
from pprint import pprint

dex = {}

with open("pokemon/pokemon.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    raw_dex = []
    for entry in reader:
        raw_dex.append(dict(entry))
        for key in raw_dex[-1]:
            try:
                raw_dex[-1][key] = int(raw_dex[-1][key])
            except ValueError:
                pass

for entry in raw_dex:
    pokemon_id = entry['id']
    dex[pokemon_id] = {}
    dex[pokemon_id]['gender_ratio'] = None
    dex[pokemon_id]['catch_rate'] = None
    dex[pokemon_id]['hatch_time'] = None
    dex[pokemon_id]['base_happiness'] = None


for entry in raw_dex:
    pokemon_id = entry['id']
    dex[pokemon_id]['pokemon_id'] = pokemon_id
    dex[pokemon_id]['identifier'] = entry['identifier']
    dex[pokemon_id]['height'] = entry['height']
    dex[pokemon_id]['weight'] = entry['weight']
    dex[pokemon_id]['base_xp'] = entry['base_experience']


with open("pokemon/pokemon_stats.csv") as csvfile:
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


with open("pokemon/pokemon_species.csv") as csvfile:
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

with open("poke_base.json",'w') as fp:
    json.dump(dex,fp,indent=4,sort_keys=True)

