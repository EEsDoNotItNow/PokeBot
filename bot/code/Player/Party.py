
from collections import defaultdict

from ..Pokemon import Monster
from ..SQL import SQL
from ..Log import Log



class Party:
    """Manage a players Monsters, their interactions, and other such things
    """


    def __init__(self, trainer_id):
        self.sql = SQL()
        self.log = Log()

        self.trainer_id = trainer_id
        self.monsters = [None, None, None, None, None, None]

        self.loaded = False


    def __len__(self):
        return len(self._monsters_not_none)


    def __iter__(self):
        for poke in self._monsters_not_none:
            yield poke


    def __contains__(self, item):
        for poke in self.monsters:
            if item == poke:
                return True
        return False


    @property
    def _monsters_not_none(self):
        return [x for x in self.monsters if x is not None]


    async def load(self):
        """Load pokes from DB
        """
        self.log.info("Loading a party")
        if self.loaded:
            self.log.warning("I think I've already been loaded before?")
        self.loaded = True
        cur = self.sql.cur
        cmd = 'SELECT * FROM trainer_party WHERE trainer_id=:trainer_id'
        value = cur.execute(cmd, self.__dict__).fetchone()
        self.log.info(value)
        for i in range(6):
            monster_id = value[f"monster_id_{i}"]
            if monster_id is not None:
                self.log.info(f"Loading Pokemon {monster_id}")
                self.monsters[i] = Monster(monster_id=monster_id)
                await self.monsters[i].load()


    async def save(self):
        """Saves party to DB
        """
        self.log.info("Saving party")
        cur = self.sql.cur
        for poke in self.monsters:
            if poke is not None:
                await poke.save()

        data = defaultdict(lambda: None)
        data['trainer_id'] = self.trainer_id
        if self.monsters[0] is not None:
            data['monster_id_0'] = self.monsters[0].monster_id
        if self.monsters[1] is not None:
            data['monster_id_1'] = self.monsters[1].monster_id
        if self.monsters[2] is not None:
            data['monster_id_2'] = self.monsters[2].monster_id
        if self.monsters[3] is not None:
            data['monster_id_3'] = self.monsters[3].monster_id
        if self.monsters[4] is not None:
            data['monster_id_4'] = self.monsters[4].monster_id
        if self.monsters[5] is not None:
            data['monster_id_5'] = self.monsters[5].monster_id
        cmd = """INSERT OR REPLACE INTO trainer_party
                (
                    trainer_id,
                    monster_id_0,
                    monster_id_1,
                    monster_id_2,
                    monster_id_3,
                    monster_id_4,
                    monster_id_5
                ) VALUES (
                    :trainer_id,
                    :monster_id_0,
                    :monster_id_1,
                    :monster_id_2,
                    :monster_id_3,
                    :monster_id_4,
                    :monster_id_5
                )"""
        cur.execute(cmd, data)
        await self.sql.commit(now=True)


    async def add(self, monster):
        """Add pokemon to the party.

        @param monster a Monster object to add to the party.

        @throws IndexError When party is already full.
        @throws ValueError Argument monster was not a Monster.
        """
        if type(monster) != Monster:
            raise ValueError
        if len(self) == 6:
            raise IndexError

        for index in range(6):
            if self.monsters[index] is None:
                break

        self.monsters[index] = monster


    async def remove(self, target):
        """
        @param target Can be Monster or Int. If Int, remove that slot's monster (zero indexed).

        @return Monster that was removed.
        """
        pass
