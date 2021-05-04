import os
from pykka import ThreadingActor

from .persister import Persister


class Writer(ThreadingActor):
    """
    Supervisor for the HTTP writer service
    """

    def __init__(self, consumer, connection):
        super().__init__()
        self.persister = Persister.start(
            consumer=consumer,
            conn=connection,
            owner=self.actor_ref
        )
