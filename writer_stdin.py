# Main entry point for the writer service

import os
import sys
import json

import psycopg3

from observatory.writer import Writer

connection = psycopg3.connect(
    'postgresql://postgres:example@localhost/postgres', autocommit=True)


Writer.start(connection=connection, consumer=map(
    json.loads, map(str.rstrip, sys.stdin)))
