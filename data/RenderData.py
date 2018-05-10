#!/usr/bin/env python3

import csv
import json
from pprint import pprint

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

pprint(species_stats)
exit()

dex = {}

for poke in raw_dex:
    entry_key = poke['id']
    dex[entry_key] = dict(poke)
    dex[entry_key]['stats'] = {}

for stats_dict in raw_stats:
    dex[stats_dict['pokemon_id']]['stats'][stats_dict['stat_id']] = {}
    dex[stats_dict['pokemon_id']]['stats'][stats_dict['stat_id']]['base'] = stats_dict['base_stat']
    dex[stats_dict['pokemon_id']]['stats'][stats_dict['stat_id']]['effort'] = stats_dict['effort']


with open("poke_base.json",'w') as fp:
    json.dump(dex,fp,indent=4)

