
import enum


class TrainerStates(enum.IntEnum):
    """
    """

    # DO NOT EDIT VALUES!
    # These are used to reference the db, and if changed will corrupt game states!
    # Offline basic states
    IDLE = 100
    BREEDING = 101
    HATCHING = 102
    RESTING = 103
    TRAINING = 104
    WORKING = 105

    # Traveling states
    FLYING = 200
    TELEPORTING = 201
    WALKING = 202
    BIKING = 203
    RUNNING = 204
    REGIONAL_TRANSITION = 205

    # Battle states
    ENCOUNTER = 300
    BATTLE = 301
    POST_BATTLE = 302

    # Interaction states
    TRADING = 400
    SHOPPING = 401
    SOMEONES_PC = 402
