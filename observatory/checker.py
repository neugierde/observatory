import os
from pykka import ThreadingActor
from kafka import KafkaProducer

from .scheduler import Scheduler
from .poller import Supervisor
from .notifier import Notifier

from .data.scheduled_site import SiteConfig


class Checker(ThreadingActor):
    """
    Supervisor for the HTTP checker service
    """

    def __init__(self, producer: KafkaProducer, topic: str, sites: list):
        super().__init__()
        me = self.actor_ref.proxy()
        self.notifier = Notifier.start(
            producer=producer, topic=topic, owner=me).proxy()
        self.pollers = Supervisor.start(
            notifier=self.notifier, owner=me).proxy()
        self.scheduler = Scheduler.start(
            sites=sites, owner=me, poller=self.pollers).proxy()
        self.scheduler.run()
