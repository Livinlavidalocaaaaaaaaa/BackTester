import backtrader as bt

class ROCStrategy(bt.Strategy):
    params = (('period', 12),)

    def __init__(self):
        self.roc = bt.indicators.RateOfChange(self.data, period=self.p.period)
        self.order_count = 0
        self.signal = None

    def next(self):
        if not self.position:
            if self.roc > 0:
                self.buy()
                self.order_count += 1
                self.signal = 1
        else:
            if self.roc < 0:
                self.sell()
                self.order_count += 1
                self.signal = 0