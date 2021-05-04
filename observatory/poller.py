import pykka
import requests
import time

from .data.scheduled_site import SiteConfig

class Poller(pykka.ThreadingActor):
    """
    This actor polls a website (given uri etc)
    """

    def __init__(self, notifier: pykka.ActorProxy, owner: pykka.ActorProxy):
        super().__init__()
        self.notifier = notifier
        self.owner = owner

    def check(self, config: SiteConfig):
        uri = config.url  # the URL to test
        re = config.re  # an options regular expression (already compiled)
        now = time.time()

        response = requests.get(uri)

        data = {
            'uri': uri,
            'status': response.status_code,
            'time': response.elapsed,
            'timestamp': now,
            'match_re': (re.search(response.text) is not None) if re else None
        }

        self.notifier.notify(data)
        self.owner.done(self.actor_ref.proxy())


class Supervisor(pykka.ThreadingActor):
    """
    Receives single requests for HTTP observations.
    Manages a pool of pollers (implementation may vary) and delegates the
    observation to one of them.
    """

    def __init__(self, notifier, owner):
        super().__init__()
        self.notifier = notifier
        self.owner = owner

    def check(self, payload: SiteConfig):
        """
        Forwards the payload to a suitable poller and returns immediately.
        """
        # starts a new poller for each check
        poller = Poller.start(notifier=self.notifier,
                              owner=self.actor_ref.proxy()).proxy()
        # alternatives:
        #   hashring: take a poller based on payload['uri']
        #   round-robin: shift a poller from the queue
        #   thread-per-uri: take or start a poller from the poller dict
        #                   using payload['uri'] as the key

        poller.check(payload)

    def done(self, poller_ref):
        """
        Recycles, or disposes of, a used poller
        """
        # stops the used poller
        poller.stop()
        # alternatives:
        #   hashring, thread-per-uri: do nothing
        #   round-robin: push to end of poller queue
