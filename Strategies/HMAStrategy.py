import backtrader as bt

class HMAStrategy(bt.Strategy):
    params = (('period', 20),)

    def __init__(self):
        self.hma = bt.indicators.HullMovingAverage(self.data, period=self.p.period)
        self.order_count = 0
        self.signal = None

    def next(self):
        if not self.position:
            if self.data.close > self.hma:
                self.buy()
                self.order_count += 1
                self.signal = 1
        elif self.data.close < self.hma:
            self.sell()
            self.order_count += 1
            self.signal = 0