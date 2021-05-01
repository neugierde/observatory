import pykka

class Notifier(pykka.ThreadingActor):
    """
    Spits out to kafka the received messages.

    The kafka client is injected.
    """

    def __init__(self, producer, owner: pykka.ActorRef):
        super().__init__()
