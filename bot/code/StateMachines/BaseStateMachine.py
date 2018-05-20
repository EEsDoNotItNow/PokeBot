


class BaseStateMachine:
    """Base class that all state machines dreive from.

    State machines handle three things.

    When created, they are run once. This allows custom state machines to do something, and then die if they are not
        needed.

    While alive, they are hit with a tick.

    While alive, they recieve any commands that the parent  couldn't handle.
    """
    def __init__(self):
        self.alive = False

        self.started = False

        # Sub state to help this state machine
        self.sub_state_machine = None


    async def command_proc(self, message):
        pass


    async def run(self):
        self.started = True
        self.alive = False


    async def tick(self):
        pass
