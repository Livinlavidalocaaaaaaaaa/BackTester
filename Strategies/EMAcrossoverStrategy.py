import backtrader as bt

class EMAcrossoverStrategy(bt.Strategy):
    params = (('fast', 10), ('slow', 30))

    def __init__(self):
        self.fast_ema = bt.indicators.EMA(self.data, period=self.p.fast)
        self.slow_ema = bt.indicators.EMA(self.data, period=self.p.slow)
        self.crossover = bt.indicators.CrossOver(self.fast_ema, self.slow_ema)
        self.order_count = 0
        self.signal = None

    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy()
                self.order_count += 1
                self.signal = 1
        elif self.crossover < 0:
            self.sell()
            self.order_count += 1
            self.signal = 0