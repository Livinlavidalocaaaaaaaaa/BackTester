import backtrader as bt

class TMAStrategy(bt.Strategy):
    params = (('period', 30),)

    def __init__(self):
        self.tma = bt.indicators.TripleExponentialMovingAverage(self.data, period=self.p.period)
        self.order_count = 0
        self.signal = None

    def next(self):
        if not self.position:
            if self.data.close > self.tma:
                self.buy()
                self.order_count += 1
                self.signal = 1
        elif self.data.close < self.tma:
            self.sell()
            self.order_count += 1
            self.signal = 0