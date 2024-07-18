import backtrader as bt

class PriceChannelsStrategy(bt.Strategy):
    params = (('period', 20),)

    def __init__(self):
        self.upper = bt.indicators.Highest(self.data.high, period=self.p.period)
        self.lower = bt.indicators.Lowest(self.data.low, period=self.p.period)
        self.order_count = 0
        self.signal = None

    def next(self):
        if not self.position:
            if self.data.close > self.upper:
                self.buy()
                self.order_count += 1
                self.signal = 1
        else:
            if self.data.close < self.lower:
                self.sell()
                self.order_count += 1
                self.signal = 0