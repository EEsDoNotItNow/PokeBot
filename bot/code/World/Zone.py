

from ..SQL import SQL
from ..Log import Log



class Zone:


    def __init__(self, zone_id):
        self.zone_id = zone_id
        self.links = {}

        self.name = None

        self.sql = SQL()
        self.log = Log()


    def __str__(self):
        return f"Zone<{self.name},{self.zone_id}>"


    def link(self, other_id, distance):
        self.links[other_id] = distance


    async def load(self):
        """Load data from DB
        """

        cur = self.sql.cur
        cmd = f"SELECT * FROM locations WHERE location_id={self.zone_id}"
        values = cur.execute(cmd).fetchone()

        self.log.info(f"Loaded: {values}")

        self.name = values['name']
