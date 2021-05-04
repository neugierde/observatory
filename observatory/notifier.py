from pykka import ThreadingActor, ActorProxy
from typing import Callable


class Notifier(ThreadingActor):
    """
    Spits out to kafka the received messages.

    The kafka client is injected.
    """

    def __init__(self, producer: Callable, owner: ActorProxy):
        super().__init__()
        self._producer = producer

    def notify(self, message: dict):
        self._producer(message)
