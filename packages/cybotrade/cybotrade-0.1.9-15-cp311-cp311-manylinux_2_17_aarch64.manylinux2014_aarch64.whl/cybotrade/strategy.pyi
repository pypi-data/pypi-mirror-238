from typing import List, Dict
from .models import (
    Candle,
    ClosedTrade,
    FloatWithTime,
    OpenedTrade,
    OrderUpdate,
    Performance,
    Interval,
)
from .runtime import StrategyTrader

import logging


class Strategy:
    """
    This class is a handler that will be used by the Runtime to handle events such as
    `on_candle_closed`, `on_order_update`, etc. The is a base class and every new strategy
    should be inheriting this class and override the methods.
    """

    logger = logging
    LOG_FORMAT: str

    def __init__(
            self,
            log_level: int = logging.INFO,
            handlers: List[logging.Handler] = [],
    ):
        """
        Set up the logger
        """

    def on_init(
            self,
            strategy: StrategyTrader,
    ):
        """
        This method is called when the strategy is started successfully.
        """

    async def on_order_update(
            self,
            strategy: StrategyTrader,
            update: OrderUpdate,
    ):
        """
        This method is called when receiving an order update from the exchange.
        """

    async def on_candle_closed(
            self,
            strategy: StrategyTrader,
            candle: Candle,
            candles: Dict[Interval, List[Candle]],
    ):
        """
        This method is called when a candle is closed for a subscribed symbol.
        """

    async def on_backtest_complete(
            self, strategy: StrategyTrader, performance: Performance
    ):
        """
        This method is called when backtest is completed.
        """

    async def on_opened_trade(
            self, strategy: StrategyTrader, opened_trade: OpenedTrade
    ):
        """
        This method is called a trade is opened.
        """

    async def on_closed_trade(
            self, strategy: StrategyTrader, closed_trade: ClosedTrade
    ):
        """
        This method is called a trade is closed.
        """

    async def on_market_update(
            self, strategy: StrategyTrader, equity: FloatWithTime, available_balance: FloatWithTime
    ):
        """
        This method is called when market stats is updated.
        """
