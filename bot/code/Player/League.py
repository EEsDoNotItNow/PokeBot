
from ..SQL import SQL
from ..Log import Log
from .Trainer import Trainer
from ..Client import Client


class League:

    trainers = []

    def __init__(self):
        self.sql = SQL()
        self.log = Log()
        self.client = Client()
        pass


    async def get_trainer(self, user_id, server_id=None):
        """Attempt to retrieve the Trainer object for a player
        @param user_id User id to look for
        @param server_id [OPTIONAL] If given, search for the unique user, if not given, return a list to use!

        @return Single trainer (if server give) or list of trainers (if no server given)
        """
        cur = self.sql.cur

        if server_id is not None:
            self.log.info("Getting trainer with server_id")
            # Check to see if we have this cached
            for trainer in self.trainers:
                if trainer.user_id == user_id and trainer.server_id == server_id:
                    return trainer

            cmd = f"SELECT trainer_id FROM trainers WHERE server_id={server_id} AND user_id={user_id}"
            value = cur.execute(cmd).fetchone()

            if value is None:
                return None

            trainer = Trainer(value['trainer_id'])

            self.trainers.append(trainer)

            return Trainer(value['trainer_id'])

        else:
            self.log.info("Getting trainer without server_id")
            # Check to see if we have this cached
            trainer_list = []
            for trainer in self.trainers:
                if trainer.user_id == user_id:
                    trainer_list.append(trainer)
                    self.log.info(f"Found trainer {trainer}")

            cmd = f"SELECT trainer_id FROM trainers WHERE user_id={user_id}"
            trainer_dicts = cur.execute(cmd).fetchall()
            self.log.info(f"Found trainer dict: {trainer_dicts}")

            for trainer in trainer_dicts:
                trainer_list.append(Trainer(trainer['trainer_id']))
                self.trainers.append(trainer_list[-1])

            if len(trainer_list) == 0:
                return None

            return trainer_list


    async def register(self, user_id, server_id):
        """Register with the league!
        """

        await Trainer.generate_trainer_tables(user_id, server_id)

        return await self.get_trainer(user_id, server_id)


    async def deregister(self, user_id, server_id):
        """Register with the league!
        """
        cur = self.sql.cur

        cmd = "SELECT trainer_id FROM trainers WHERE server_id=:server_id AND user_id=:user_id"
        value = cur.execute(cmd, locals()).fetchone()
        if value is None:
            return False

        # Sorry dude, you are getting BALETED
        cmd = "DELETE FROM trainers WHERE server_id=:server_id AND user_id=:user_id"
        cur.execute(cmd, locals())
        await self.sql.commit()

        return True
