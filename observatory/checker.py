import os
import pykka
import kafka

from .scheduler import Scheduler
from .poller import Supervisor
from .notifier import Notifier


class Checker(pykka.ThreadingActor):
    """
    Supervisor for the HTTP checker service
    """

    def __init__(self, producer: kafka.KafkaProducer, topic: str, sites: dict):
        super().__init__()
        me = self.actor_ref.proxy()
        self.scheduler = Scheduler.start(
            sites=sites, owner=me)
        self.notifier = Notifier.start(
            producer=producer, topic=topic, owner=me)
        self.pollers = Supervisor.start(
            notifier=self.notifier.proxy(), owner=me)
