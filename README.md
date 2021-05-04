Observatory
===========

A little actor-based system to check for site health through HTTP.

It is composed by two parts:

- A **checker** that will check for site health and notify results through Kafka
- A **writer** that will consume messages form Kafka and persist them to a PG DB 

Start each process with
```
python checker.py
python writer.py
```

Configuration
-------------

Connection with external services is configured by environment variables:

- `PG_CONNECTION`: Provide a postgres-compatible connection string
- `KAFKA_HOST`: Provide the host+port to connect kafka
- `KAFKA_TOPIC`: The topic to use for messaging
- `SITES_CONFIG`: The path to a toml configuration with the sites to check

The config file has the following structure:

```toml
[optional title]
url = "https://required.host/path"

# Time between checks in seconds, default is 600
every = 600 

# Optional regular expression to check. It will be compiled as-is
re = "some content"

[another site]
url = "https://required.host/path"

# Time between checks in seconds, default is 600
every = 86400

```


Implementation details
----------------------

The `Supervisor` class in `observatory.poller` module can implement several
pooling strategies, but without testing at scale it's not worth to see if
there is an actuall contention because of threads.

The system has not been tested with a real Kafka, instead I have used 
stdin/stdout to simulate a message queue. Lines correspond to messages.

To start the pg-only simulation, use

```sh
python checker_stdout.py | python writer_stdin.py
```

A docker-compose configuration is provided to start a postgres instance.