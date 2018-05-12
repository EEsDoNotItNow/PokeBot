

from ..Log import Log
from ..SQL import SQL

from .Zone import Zone

class World:


    def __init__(self):
        # Regions are mapped with id: obj
        self.zones = {}

        self.log = Log()
        self.sql = SQL()

        self.link_regions()


    def link_regions(self):

        cur = self.sql.cur
        cmd = "SELECT * FROM locations"
        zones = cur.execute(cmd).fetchall()

        cmd = "SELECT * FROM zone_connections"
        zone_connections = cur.execute(cmd).fetchall()

        for connection in zone_connections:
            self.log.info(connection)

            zone1_id = connection['location_id_1']
            zone2_id = connection['location_id_2']

            if zone1_id not in self.zones:
                self.zones[zone1_id] = Zone(zone1_id)

            if zone2_id not in self.zones:
                self.zones[zone2_id] = Zone(zone2_id)

            self.zones[connection['location_id_1']].link(connection['location_id_2'], connection['distance'])
            self.zones[connection['location_id_2']].link(connection['location_id_1'], connection['distance'])
        
