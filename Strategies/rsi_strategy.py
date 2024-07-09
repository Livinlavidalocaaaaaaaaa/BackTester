import backtrader as bt

class RSIStrategy(bt.Strategy):
    params = (('period', 14), ('overbought', 70), ('oversold', 30))

    def __init__(self):
        self.rsi = bt.indicators.RSI(period=self.p.period)
        self.order_count = 0
        self.signal = None

    def next(self):
        if not self.position:
            if self.rsi < self.p.oversold:
                self.buy()
                self.order_count += 1
                self.signal = 1
        elif self.rsi > self.p.overbought:
            self.close()
            self.order_count += 1
            self.signal = 0
