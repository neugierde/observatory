import pykka
from time import time, sleep
from heapq import heappush, heapify, heappop

from .data.scheduled_site import SiteConfig


class Scheduler(pykka.ThreadingActor):
    """
    Manages a sorted set of future actions (observe an HTTP address).

    When the expected time comes, a message is sent out, and the action is
    enqueued again at the right time.
    """

    def __init__(self, sites: list, owner: pykka.ActorProxy, poller: pykka.ActorProxy):
        super().__init__()
        self.owner = owner
        self.poller = poller
        self.sites = [SiteConfig(s).schedule() for s in sites]
        heapify(self.sites)

    def run(self):
        next_site = heappop(self.sites)
        now = time()
        if next_site.schedule > now:
            sleep(next_site.schedule - now)

        self.poller.check(next_site.config)

        heappush(self.sites, next_site.next_schedule())
        self.proxy().run()
