from datetime import timedelta

from abc import ABC, abstractmethod

from proalgotrader_protocols.chart import Chart_Protocol
from proalgotrader_protocols.symbol import Symbol_Protocol


class Store_Protocol(ABC):
    @abstractmethod
    async def add_chart(self, symbol: Symbol_Protocol, timeframe: timedelta) -> Chart_Protocol:
        ...

    async def boot(self) -> None:
        ...

    async def run(self) -> None:
        ...
