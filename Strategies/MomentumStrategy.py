import backtrader as bt

class MomentumStrategy(bt.Strategy):
    params = (('period', 10),)

    def __init__(self):
        self.momentum = bt.indicators.Momentum(self.data, period=self.p.period)
        self.order_count = 0
        self.signal = None

    def next(self):
        if not self.position:
            if self.momentum > 0:
                self.buy()
                self.order_count += 1
                self.signal = 1
        else:
            if self.momentum < 0:
                self.sell()
                self.order_count += 1
                self.signal = 0