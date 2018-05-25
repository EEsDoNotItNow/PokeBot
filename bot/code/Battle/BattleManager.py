
from .Battle import Battle


class BattleManager:

    battles = []

    @classmethod
    def get_battle(cls, battle_id=None):

        # Check to see if we can remove old battles
        cls.battles = [x for x in cls.battles if x.active or len(x.participants)]

        if battle_id is None:
            new_battle = Battle()
            cls.battles.append(new_battle)
            return new_battle
        else:
            for battle in cls.battles:
                if battle.battle_id == battle_id:
                    return battle
            raise ValueError(f"I don't see a battle with id {battle_id}")
