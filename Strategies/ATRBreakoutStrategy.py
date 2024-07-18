import backtrader as bt

class ATRBreakoutStrategy(bt.Strategy):
    params = (('period', 14), ('multiplier', 2))

    def __init__(self):
        self.atr = bt.indicators.ATR(self.data, period=self.p.period)
        self.order_count = 0
        self.signal = None

    def next(self):
        if not self.position:
            if self.data.close > self.data.close[-1] + self.p.multiplier * self.atr:
                self.buy()
                self.order_count += 1
                self.signal = 1
        else:
            if self.data.close < self.data.close[-1] - self.p.multiplier * self.atr:
                self.sell()
                self.order_count += 1
                self.signal = 0