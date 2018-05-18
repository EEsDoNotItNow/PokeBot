#!/bin/bash

pipenv install --dev
pipenv run nosetests --timer-ok 1s --timer-warning 5s --with-timer
