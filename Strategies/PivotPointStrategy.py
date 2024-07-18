import backtrader as bt

class PivotPointStrategy(bt.Strategy):
    def __init__(self):
        self.pivot = bt.indicators.PivotPoint(self.data)
        self.order_count = 0
        self.signal = None

    def next(self):
        if not self.position:
            if self.data.close > self.pivot.r1[0]:
                self.buy()
                self.order_count += 1
                self.signal = 1
        else:
            if self.data.close < self.pivot.s1[0]:
                self.sell()
                self.order_count += 1
                self.signal = 0