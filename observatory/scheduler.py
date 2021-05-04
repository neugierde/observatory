from time import time, sleep
from heapq import heappush, heapify, heappop

from pykka import ThreadingActor, ActorProxy

from .data.scheduled_site import SiteConfig


class Scheduler(ThreadingActor):
    """
    Manages a sorted set of future actions (observe an HTTP address).

    When the expected time comes, a message is sent out, and the action is
    enqueued again at the right future time.
    """

    def __init__(self, sites: list, owner: ActorProxy, poller: ActorProxy):
        super().__init__()
        self._owner = owner
        self._poller = poller
        self.sites = [SiteConfig(**s).schedule() for s in sites]

        heapify(self.sites)

    def run(self):
        next_site = heappop(self.sites)
        now = time()

        if next_site.schedule > now:
            sleep(next_site.schedule - now)

        self._poller.check(next_site.config)

        heappush(self.sites, next_site.next_schedule())
        self.actor_ref.proxy().run()
