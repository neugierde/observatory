import os
import pykka

from scheduler import Scheduler
from poller import Supervisor
from notifier import Notifier


class Checker(pykka.ThreadingActor):
    """
    Supervisor for the HTTP checker service
    """

    def __init__(self, producer, sites: dict):
        super().__init__()
        self.pollers = Supervisor.start(owner=self.actor_ref)
        self.scheduler = Scheduler.start(sites=sites, owner=self.actor_ref)
        self.notifier = Notifier.start(producer=producer, owner=self.actor_ref)
