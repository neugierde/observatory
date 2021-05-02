import pykka
import kafka


class Notifier(pykka.ThreadingActor):
    """
    Spits out to kafka the received messages.

    The kafka client is injected.
    """

    def __init__(self, producer: kafka.KafkaProducer, topic: str, owner: pykka.ActorRef):
        super().__init__()
        self.producer = producer
        self.topic = topic

    def notify(self, message: dict):
        self.producer.send(self.topic, value=message)
