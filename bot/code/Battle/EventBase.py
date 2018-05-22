


class EventBase:
    """Define the base event for battle events.
    """


    def __init__(self):

        # Mark when event has been used.
        self.triggered = False

        # Mark even ready for processing
        self.ready = False

        #
        self.turns = -1
        pass


    def setup(self):
        """This event is ready for use, mark it as such
        """
        self.ready = True


    def execute(self, battle, *args, **kwargs):
        """ Implement in other classes. Depending on the event,
        """
        raise NotImplementedError()


    def tear_down(self):
        """This event has been run, prevent another run before a setup
        """
        if self.triggered or not self.ready:
            raise RuntimeError(f"{self} was not ready! Triggered state: {self.triggered} Ready state: {self.ready}")
        self.triggered = True
