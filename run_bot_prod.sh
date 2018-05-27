#!/bin/bash

# .creds file should look like this
# export CLIENT_TOKEN="LOTS OF NUMBERS THAT MAKE A TOKEN GO HERE"

git pull
source ~/.ssh/pokebot.discord.prod.creds
pipenv run python ./Bot.py --env prod "$@"
