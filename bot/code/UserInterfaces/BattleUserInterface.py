

from .BaseUserInterface import BaseUserInterface



class BattleUserInterface(BaseUserInterface):
    """"Handle a pokemon battle
    """

    def __init__(self, trainer, opponent):
        super().__init__()
        raise NotImplementedError()
        self.alive = True

        self.trainer = trainer

        self.opponent = opponent


    async def run(self):
        raise NotImplementedError()


    async def command_proc(self, message):
        raise NotImplementedError()


    async def tick(self):
        raise NotImplementedError()
