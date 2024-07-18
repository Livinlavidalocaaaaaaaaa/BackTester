import backtrader as bt

class TripleMovingAverageCrossover(bt.Strategy):
    params = (('fast', 5), ('medium', 20), ('slow', 50))

    def __init__(self):
        self.fast_ma = bt.indicators.SMA(period=self.p.fast)
        self.medium_ma = bt.indicators.SMA(period=self.p.medium)
        self.slow_ma = bt.indicators.SMA(period=self.p.slow)
        self.order_count = 0
        self.signal = None

    def next(self):
        if not self.position:
            if self.fast_ma > self.medium_ma and self.medium_ma > self.slow_ma:
                self.buy()
                self.order_count += 1
                self.signal = 1
        elif self.fast_ma < self.medium_ma and self.medium_ma < self.slow_ma:
            self.close()
            self.order_count += 1
            self.signal = 0