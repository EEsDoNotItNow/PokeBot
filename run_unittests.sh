#!/bin/bash

pipenv install --user
pipenv run nosetests --timer-ok 1s --timer-warning 5s --with-timer
