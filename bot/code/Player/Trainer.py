

import discord
import datetime

from ..Client import Client
from ..Log import Log

class Trainer:

    def __init__(self, trainer_id):
        self.trainer_id = trainer_id
        self.client = Client()
        self.log = Log()


    async def get_trainer_card(self):
        em = discord.Embed()

        server = self.client.get_server(self.server_id)
        member = server.get_member(self.user_id)

        em.title = "Trainer Card"

        if member.nick:
            em.set_author(name=member.nick)
        else:
            em.set_author(name=member.name)

        em.add_field(name="Level", value=0)

        em.add_field(name="Pokedex", value="15/75")

        em.add_field(name="Leader", value="Bolt (Pikachu) L.25")

        em.timestamp = datetime.datetime.now()

        return em