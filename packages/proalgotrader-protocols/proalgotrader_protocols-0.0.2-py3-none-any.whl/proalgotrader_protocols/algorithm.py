from abc import abstractmethod
from datetime import timedelta
from typing import Literal, Tuple

from proalgotrader_protocols.enums.account_type import AccountType
from proalgotrader_protocols.chart import Chart_Protocol
from proalgotrader_protocols.store import Store_Protocol
from proalgotrader_protocols.symbol import Symbol_Protocol


class Algorithm_Protocol(Store_Protocol):
    def set_account_type(self, account_type: AccountType) -> None:
        ...

    @abstractmethod
    async def initialize(self) -> None:
        ...

    @abstractmethod
    async def next(self) -> None:
        ...

    def add_equity(self, symbol_key: str) -> Symbol_Protocol:
        ...

    def add_future(
        self, symbol_key: str, expiry_input: Tuple[Literal["weekly", "monthly"], int]
    ) -> Symbol_Protocol:
        ...

    def add_option(
        self, symbol_key: str, expiry_input: Tuple[Literal["weekly", "monthly"], int], strike_price_input: int,
    ) -> Symbol_Protocol:
        ...

    async def add_chart(self, symbol: Symbol_Protocol, timeframe: timedelta) -> Chart_Protocol:
        ...
