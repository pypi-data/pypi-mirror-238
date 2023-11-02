import datetime
from typing import Dict, Protocol

from proalgotrader_protocols.chart import Chart_Protocol
from proalgotrader_protocols.feed import Feed_Protocol


class Broker_Protocol(Protocol):
    name: str
    mode: str
    resolutions: Dict[datetime.timedelta, str]

    def __init__(self, config: Dict[str, str]) -> None:
        ...

    def get_feed(self, chart: Chart_Protocol) -> Feed_Protocol:
        ...
