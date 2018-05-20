
# from ..SQL import SQL
from ..Player import TrainerStates as TS

from .BaseStateMachine import BaseStateMachine



class EncounterStateMachine(BaseStateMachine):
    """"Handle a pokemon battle
    """

    def __init__(self, trainer, opponent):
        super().__init__()
        # raise NotImplementedError()
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

        self.user = await self.client.get_user_info(self.trainer.user_id)

        await self.client.start_private_message(self.user)

        for channel in self.client.private_channels:
            if channel.user == self.user:
                break
        self.channel = channel

        while True:
            self.action = None

            # Print opponents Pokemon
            embed = await self.opponent.em()
            await self.client.send_message(self.channel, embed = embed)
            # Print users Pokemon
            poke = await self.trainer.party.get_leader()
            embed = await poke.em()
            await self.client.send_message(self.channel, embed = embed)

            prompt_question = "What would you like to do?"
            prompt_list = ["Fight", "Items", "Pokemon", "Run"]
            selection = await self.client.select_prompt(self.channel,
                                                        prompt_question,
                                                        prompt_list,
                                                        user=self.user,
                                                        timeout=300)
            menu_list = [
                self._menu_fight,
                self._menu_item,
                self._menu_pokemon,
                self._menu_run]

            await menu_list[selection]()

            await self.client.send_message(self.channel,
                                           "This is a proof of concept, and doesn't do anything yet!")
            break

            if self.action is None:
                continue
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
        pass
        """
            Get active poke
            Request current move set
            Ask user to pick one, or cancel
            Register action
        """


    async def _menu_item(self):
        pass
        """
            Get inventory
            Request player pick an item, or cancel
            Register action
        """


    async def _menu_pokemon(self):
        pass
        """
            Get party
            Request player pick a poke
            Give details, or make active
            Register action
        """


    async def _menu_run(self):
        pass
        """
            Prompt user to run
            Register action
        """
