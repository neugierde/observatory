import pykka

class Persister(pykka.ThreadingActor):
    """
    Reads from kafka and persists to a PG database
    """

    pass
