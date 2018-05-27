#!/bin/bash

# .creds file should look like this
# export CLIENT_TOKEN="LOTS OF NUMBERS THAT MAKE A TOKEN GO HERE"

source ~/.ssh/pokebot.discord.dev.creds
pipenv run python -B ./Bot.py --env dev "$@"
