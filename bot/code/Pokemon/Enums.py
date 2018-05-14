

import enum

from enum import auto


class EnumStatus(enum.Flag):
    ALIVE = auto()
    DEAD = auto()
    FROZEON = auto()
    SLEEP = auto()
    PARALYZED = auto()
    BURNED = auto()
    FLINCH = auto()
    CONFUSED = auto()
    INFATUATION = auto()
    LEECHSEED = auto()
