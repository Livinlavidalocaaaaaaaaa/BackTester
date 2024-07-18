import backtrader as bt

class GuppyMultipleMovingAverageStrategy(bt.Strategy):
    params = (
        ('fast_periods', (3, 5, 8, 10, 12, 15)),  # Fast EMA periods
        ('slow_periods', (30, 35, 40, 45, 50, 60)),  # Slow EMA periods
    )

    def __init__(self):
        self.fast_emas = [bt.indicators.EMA(self.data.close, period=period) for period in self.p.fast_periods]
        self.slow_emas = [bt.indicators.EMA(self.data.close, period=period) for period in self.p.slow_periods]
        
        # Crossover indicators
        self.fast_cross = bt.indicators.CrossOver(self.fast_emas[0], self.fast_emas[-1])
        self.slow_cross = bt.indicators.CrossOver(self.slow_emas[0], self.slow_emas[-1])
        
        self.order_count = 0
        self.signal = 0
        self.initial_cash = self.broker.getvalue()
        self.log(f"Initial cash: {self.initial_cash}")

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()} {txt}')

    def next(self):
        fast_bullish = all(ema1 > ema2 for ema1, ema2 in zip(self.fast_emas[:-1], self.fast_emas[1:]))
        fast_bearish = all(ema1 < ema2 for ema1, ema2 in zip(self.fast_emas[:-1], self.fast_emas[1:]))
        slow_bullish = all(ema1 > ema2 for ema1, ema2 in zip(self.slow_emas[:-1], self.slow_emas[1:]))
        slow_bearish = all(ema1 < ema2 for ema1, ema2 in zip(self.slow_emas[:-1], self.slow_emas[1:]))

        if not self.position:
            if fast_bullish and slow_bullish and self.fast_cross > 0:
                self.buy()
                self.order_count += 1
                self.signal = 1
                self.log(f"BUY EXECUTED, Price: {self.data.close[0]:.2f}")
        else:
            if fast_bearish and slow_bearish and self.fast_cross < 0:
                self.sell()
                self.order_count += 1
                self.signal = -1
                self.log(f"SELL EXECUTED, Price: {self.data.close[0]:.2f}")

    def stop(self):
        self.roi = (self.broker.getvalue() / self.initial_cash) - 1.0
        self.log(f'ROI: {self.roi:.2%}')
        self.log(f'Final Value: {self.broker.getvalue():.2f}')