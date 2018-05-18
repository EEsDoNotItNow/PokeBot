

from .BaseStateMachine import BaseStateMachine



class BattleStateMachine(BaseStateMachine):
    """"Handle a pokemon battle
    """

    def __init__(self, trainer_id, opponent_id):
        super().__init__()
        raise NotImplementedError()


    async def command_proc(self, message):
        raise NotImplementedError()


    async def tick(self):
        raise NotImplementedError()
