from dataclasses import dataclass, field, replace
from time import time, sleep
from re import Pattern, compile
from typing import Union


@dataclass
class SiteConfig:
    url: str
    title: str = ''
    every: int = 300
    re: Union[Pattern, str, None] = None

    def __post_init__(self):
        if isinstance(self.re, str):
            self.re = compile(self.re)

    def schedule(self) -> 'ScheduledSite':
        return ScheduledSite(config=self)


@dataclass(order=True)
class ScheduledSite:
    config: SiteConfig = field(compare=False)
    schedule: float = field(default_factory=lambda: time())

    def next_schedule(self) -> 'ScheduledSite':
        return replace(self, schedule=self.schedule + self.config.every)
