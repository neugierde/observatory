import requests
import time

from pykka import ThreadingActor, ActorProxy

from .data.scheduled_site import SiteConfig

class Poller(ThreadingActor):
    """
    This actor polls a website (given uri etc). When done, sends a message
    to the notifier with the observation, and calls back the owner to
    perform disposal.
    """

    def __init__(self, notifier: ActorProxy, owner: ActorProxy):
        super().__init__()
        self._notifier = notifier
        self._owner = owner

    def check(self, config: SiteConfig):
        uri = config.url
        re = config.re
        now = time.time()

        response = requests.get(uri)
        data = {
            'uri': uri,
            'status': response.status_code,
            'time': response.elapsed.total_seconds(),
            'timestamp': now,
            'match_re': (re.search(response.text) is not None) if re else None
        }

        self._notifier.notify(data)
        self._owner.done(self.actor_ref.proxy())


class Supervisor(ThreadingActor):
    """
    Receives single requests for HTTP observations.
    Manages a pool of pollers (implementation may vary) and delegates the
    observation to one of them.
    """

    def __init__(self, notifier: ActorProxy, owner: ActorProxy):
        super().__init__()
        self._notifier = notifier
        self._owner = owner
        print("starting", self)

    def check(self, payload: SiteConfig):
        """
        Forwards the payload to a suitable poller and returns immediately.
        """
        # starts a new poller for each check
        poller = Poller.start(notifier=self._notifier,
                              owner=self.actor_ref.proxy()).proxy()
        # alternatives:
        #   hashring: take a poller based on payload['uri']
        #   round-robin: shift a poller from the queue
        #   thread-per-uri: take or start a poller from the poller dict
        #                   using payload['uri'] as the key

        poller.check(payload)

    def done(self, poller: ActorProxy):
        """
        Recycles, or disposes of, a used poller
        """
        # stops the used poller
        poller.stop()
        # alternatives:
        #   hashring, thread-per-uri: do nothing
        #   round-robin: push to end of poller queue
