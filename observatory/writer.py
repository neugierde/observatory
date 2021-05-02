import os
import pykka

from .persister import Persister


class Writer(pykka.ThreadingActor):
    """
    Supervisor for the HTTP writer service
    """

    def __init__(self, consumer, connection):
        super().__init__()
        self.persister = Persister.start(
            consumer=consumer,
            owner=self.actor_ref
        )
