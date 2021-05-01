import pykka


class Scheduler(pykka.ThreadingActor):
    """
    Manages a sorted set of future actions (observe an HTTP address).

    When the expected time comes, a message is sent out, and the action is
    enqueued again at the right time.

    It may support different frequency, depending on the implementation
    """

    def __init__(self, sites: dict, owner: pykka.ActorRef):
        super().__init__()
        self.sites = sites
