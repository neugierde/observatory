from typing import Any, Iterable

from pykka import ThreadingActor, ActorProxy


class Persister(ThreadingActor):
    """
    Reads from kafka and persists to a PG database
    """

    migration = """
    CREATE TABLE IF NOT EXISTS observations (
        id serial,
        title text NOT NULL,
        uri text NOT NULL,
        status integer NOT NULL,
        time real NOT NULL,
        timestamp real NOT NULL,
        match_re boolean
    );
    """

    fields = ['title', 'uri', 'status', 'time', 'timestamp', 'match_re']
    sql = 'INSERT INTO observations (title, uri, status, time, timestamp, match_re) VALUES (%s, %s, %s, %s, %s, %s::boolean);'

    def __init__(self, owner: ActorProxy, conn: Any, consumer: Iterable[dict]):
        super().__init__()
        self._owner = owner
        self.conn = conn
        self.consumer = consumer

    def on_start(self):
        print("consuming...")
        with self.conn.cursor() as cur:
            for msg in self.consumer:
                print("received", msg)
                # values = [msg.get(field) for field in self.fields]
                values = [msg['title'], msg['uri'], msg['status'], msg['time'], msg['timestamp'], msg['match_re']]
                print("received", values)
                # optimization: use `execute_many`
                cur.execute(Persister.sql, values)

    @classmethod
    def migrate(cls, conn):
        with conn.cursor() as cur:
            cur.execute(Persister.migration)

