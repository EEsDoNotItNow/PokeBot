

import enum

from enum import auto


class EnumStatus(enum.Flag):
    ALIVE = auto()
    DEAD = auto()
    FAINT = auto()
    FROZEON = auto()
    SLEEP = auto()
    PARALYZED = auto()
    BURNED = auto()
    FLINCH = auto()
    CONFUSED = auto()
    INFATUATION = auto()
    LEECHSEED = auto()


class EnumMoveCategory(enum.Flag):
    ATTACK = auto()
    STATUS_EFFECT = auto()
    IS_MULTI_ROUND = auto()
    HAS_COOLDOWN = auto()


class EnumMoveTarget(enum.IntEnum):
    SPECIFIC_MOVE = 1
    SELECTED_POKEMON_ME_FIRST = 2
    ALLY = 3
    USERS_FIELD = 4
    USER_OR_ALLY = 5
    OPPONENTS_FIELD = 6
    USER = 7
    RANDOM_OPPONENT = 8
    ALL_OTHER_POKEMON = 9
    SELECTED_POKEMON = 10
    ALL_OPPONENTS = 11
    ENTIRE_FIELD = 12
    USER_AND_ALLIES = 13
    ALL_POKEMON = 14
