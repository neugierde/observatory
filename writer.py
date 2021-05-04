# Main entry point for the writer service

import os
import json

import psycopg3

from kafka import KafkaConsumer

from observatory.writer import Writer

connection = psycopg3.connect(
    os.getenv('PG_CONNECTION', 'dbname=test user=postgres')
)

consumer = KafkaConsumer(
    os.getenv('KAFKA_TOPIC', 'localhost:9092'),
    bootstrap_servers=[os.getenv('KAFKA_HOST', 'localhost:9092')],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

Writer.start(connection=connection, consumer=consumer)
