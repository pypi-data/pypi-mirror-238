import pandas as pd

from datetime import timedelta
from typing import Callable, Protocol

from proalgotrader_protocols.indicator import Indicator_Protocol
from proalgotrader_protocols.symbol import Symbol_Protocol


class Chart_Protocol(Protocol):
    def __init__(self, symbol: Symbol_Protocol, timeframe: timedelta, algo_session, broker) -> None:
        ...

    data: pd.DataFrame | pd.Series

    async def add_indicator(
        self, key:str, fn: Callable[[pd.DataFrame], pd.DataFrame | pd.Series | None]
    ) -> Indicator_Protocol:
        ...
