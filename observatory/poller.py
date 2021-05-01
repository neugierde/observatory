import pykka

class Poller(pykka.ThreadingActor):
    """
    This actor polls a website (given )
    """

    pass


class Supervisor(pykka.ThreadingActor):
    """
    Receives single requests for HTTP observations.
    Manages a pool of pollers (implementation may vary) and delegates the
    observation to one of them.
    """

    pass
