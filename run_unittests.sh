#!/bin/bash

# .creds file should look like this
# export CLIENT_TOKEN="LOTS OF NUMBERS THAT MAKE A TOKEN GO HERE"

source ~/.ssh/pokebot.discord.creds
pipenv run nosetests --timer-ok 1s --timer-warning 5s --with-timer
