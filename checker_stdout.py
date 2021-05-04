# stdout-based checker

import os

import json
import toml

from observatory.checker import Checker

sites = [dict(title=k, **v)
         for k, v in toml.load(os.getenv('SITES_CONFIG', 'config/sites.toml')).items()]

Checker.start(
    producer=lambda value: print(json.dumps(value)),
    sites=sites
)
