

from ..SQL import SQL
from ..Log import Log



class Zone:


    def __init__(self, zone_id):
        self.zone_id = zone_id
        self.links = {}

        self.sql = SQL()
        self.log = Log()


    def link(self, other_id, distance):
        self.links[other_id] = distance


    async def load(self):
        """Load data from DB
        """

        cur = self.sql.cur
        cmd = "SELECT * FROM locations"
        data = cur.execute(cmd).fetchone()

        self.log.info("Loaded data")
