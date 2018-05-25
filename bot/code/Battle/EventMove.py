

from ..Pokemon.Enums import EnumMoveCategory as MC

from .EventBase import EventBase



class EventMove(EventBase):


    def __init__(self, move):
        """Given a Move object, create a new even to handle this attack.
        """
        self.move = move


    def execute(self, battle, *args, **kwargs):
        """ Implement in other classes. Depending on the event,
        """
        print(MC)
