

from ..Player import TrainerStates as TS

from .BaseStateMachine import BaseStateMachine



class EncounterStateMachine(BaseStateMachine):
    """"Handle a pokemon battle
    """

    def __init__(self, trainer, opponent):
        super().__init__()
        raise NotImplementedError()
        self.alive = True

        self.trainer = trainer

        self.opponent = opponent


    async def run(self):

        self.started = True
        self.log.info(f"{self.trainer.trainer_id} Begin our run of {self.__class__.__name__}")
        old_state = self.trainer.state
        self.trainer.state = TS.ENCOUNTER
        try:
            await self._run()
        except Exception:
            self.log.exception(f"{self.trainer.trainer_id} Something went wrong...")
            self.alive = False

        # TODO: We really should set this to a post battle event...
        self.trainer.state = old_state
        await self.trainer.save()
        self.log.info(f"{self.trainer.trainer_id} Saved status and exited {self.__class__.__name__}")


    async def _run(self):
        pass

        return

        while True:
            pass
            """
                Present menu
                    Fight
                    Item
                    Pokemon
                    Run

                Handle Actions on both sides

                Determine if fight is over, exit if so
                    Did players pokemon feint?
                        Yes: Can we swap in another?
                            Yes: Prompt user and handle results
                            No: Send to pokemon center
                        No: Send to pokemon center
                    Did the opponent feint?
                        Yes: Exit battle
                        No: Keep fighting!
            """


    async def _menu_fight(self):
        raise NotImplementedError()
        """
            Get active poke
            Request current move set
            Ask user to pick one, or cancel
            Register action
        """


    async def _menu_item(self):
        raise NotImplementedError()
        """
            Get inventory
            Request player pick an item, or cancel
            Register action
        """


    async def _menu_pokemon(self):
        raise NotImplementedError()
        """
            Get party
            Request player pick a poke
            Give details, or make active
            Register action
        """


    async def _menu_run(self):
        raise NotImplementedError()
        """
            Prompt user to run
            Register action
        """
