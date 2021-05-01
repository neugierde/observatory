# Main entry point for the checker service

import os

import json
import toml

from kafka import KafkaProducer

from observatory.checker import Checker

producer = KafkaProducer(
    bootstrap_servers=[os.getenv('KAFKA_HOST', 'localhost:9092')],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

sites = toml.load(os.getenv('SITES_CONFIG', '../config/sites.toml'))

Checker.start(producer=producer, sites=sites)
