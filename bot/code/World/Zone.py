

class Zone:


    def __init__(self, zone_id):
        self.zone_id = zone_id
        self.links = {}


    def link(self, other_id, distance):
        self.links[other_id] = distance

