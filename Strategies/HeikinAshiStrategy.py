import backtrader as bt

class HeikinAshiStrategy(bt.Strategy):
    def __init__(self):
        self.ha = bt.indicators.HeikinAshi(self.data)
        self.order_count = 0
        self.signal = None

    def next(self):
        if not self.position:
            if self.ha.ha_close > self.ha.ha_open:
                self.buy()
                self.order_count += 1
                self.signal = 1
        elif self.ha.ha_close < self.ha.ha_open:
            self.sell()
            self.order_count += 1
            self.signal = 0