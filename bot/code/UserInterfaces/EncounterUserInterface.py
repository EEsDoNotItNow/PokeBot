
from ..Battle import BattleManager
from ..Battle.Events import EventRun
from ..Client import EmojiMap
from ..Player import TrainerStates as TS

from .BaseUserInterface import BaseUserInterface


class EncounterUserInterface(BaseUserInterface):
    """"Handle a pokemon battle
    """

    def __init__(self, trainer, opponent):
        super().__init__()
        # raise NotImplementedError()
        self.alive = True

        self.battle = BattleManager.get_battle()

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
        finally:
            try:
                await self.battle.deregister(self.trainer)
            except ValueError:
                self.log.exception("Failed to deregister, that's weird!")

        # TODO: We really should set this to a post battle event...
        self.trainer.state = old_state
        await self.trainer.save()
        self.log.info(f"{self.trainer.trainer_id} Saved status and exited {self.__class__.__name__}")


    async def _run(self):

        self.user = await self.client.get_user_info(self.trainer.user_id)

        await self.client.start_private_message(self.user)

        for channel in self.client.private_channels:
            if channel.user == self.user:
                break
        self.channel = channel

        while self.battle.active:
            self.action = None

            # Print opponents Pokemon
            card = await self.opponent.text_card(opponent=True)
            await self.client.send_message(self.channel, card)
            # Print users Pokemon
            poke = await self.trainer.party.get_leader()
            card = await poke.text_card()
            await self.client.send_message(self.channel, card)

            emap = EmojiMap()

            question = "What do you want to do?"
            responses = (
                (emap(":fist:"), "Fight"),
                (emap(":package:"), "Use Item"),
                # (emap(":pokeball:"), "Use Pokemon"),
                (emap(":runner:"), "Run away"),
            )

            selection = await self.client.select_custom_prompt(self.channel, question, responses, self.user)

            await self.client.send_message(self.channel, f"You picked {responses[selection][1]}")

            # prompt_question = "What would you like to do?"
            # prompt_list = ["Fight", "Items", "Pokemon", "Run"]
            # selection = await self.client.select_prompt(self.channel,
            #                                             prompt_question,
            #                                             prompt_list,
            #                                             user=self.user,
            #                                             timeout=300)
            menu_list = [
                self._menu_fight,
                self._menu_item,
                # self._menu_pokemon,
                self._menu_run]

            picked_action = await menu_list[selection]()

            if not picked_action:
                continue

            await self.battle.execute()

            self.log.info(f"Attemping to pull from turn {self.battle.turn} - 1")

            for log in await self.battle.get_log(self.battle.turn - 1):
                await self.client.send_message(self.channel, log)

            # Item actions happen

            # Pokemon swaps happen

            # Battle actions are checked for who goes first

            # First attack
            # Check for swap

            # Second attack
            # Check for swap

            """
                Present menu
                    [ ] Fight
                    [ ] Item
                    [ ] Pokemon
                    [x] Run

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
            Register action ("fight", n)
        """


    async def _menu_item(self):
        pass
        """
            Get inventory
            Request player pick an item, or cancel
            Register action ("use", n, m) or ("give", n, m) or ("take", n)
        """


    async def _menu_pokemon(self):
        pass
        """
            Get party
            Request player pick a poke
            Give details, or make active
            Register action ("swap", n, m)
        """


    async def _menu_run(self):
        """
            Prompt user to run
            Register action
        """
        try:
            choice = await self.client.confirm_prompt(self.channel, "Do you want to run away?", user=self.user)
        except TimeoutError:
            return False

        if choice:
            await self.battle.register_event(EventRun(self.battle, self.trainer))
        return True
