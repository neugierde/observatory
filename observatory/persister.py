from typing import Any

from kafka import KafkaConsumer
from pykka import ThreadingActor, ActorProxy


class Persister(ThreadingActor):
    """
    Reads from kafka and persists to a PG database
    """

    migration = """
    CREATE TABLE IF NOT EXISTS observations (
        id serial
        uri text NOT NULL,
        status integer NOT NULL,
        time real NOT NULL,
        timestamp real NOT NULL,
        match_re boolean
    );
    """

    fields = ['uri', 'status', 'time', 'timestamp', 'match_re']
    sql = 'INSERT INTO observations (uri, status, time, timestamp, match_re) VALUES (%s, %s, %s, %s, %s::boolean);'

    def __init__(self, owner: ActorProxy, conn: Any, consumer: KafkaConsumer):
        super().__init__()
        self._owner = owner
        self.conn = conn
        self.consumer = consumer

    def run(self):
        with self.conn.cursor() as cur:
            for msg in self.consumer:
                values = tuple(msg.get(field) for field in Persister.fields)
                # optimization: use `execute_many`
                cur.execute(Persister.sql, values)
                self.conn.commit()

    @classmethod
    def create_table(cls, conn):
        with conn.cursor() as cur:
            cur.execute(Persister.migration)

