import backtrader as bt

class MACDStrategy(bt.Strategy):
    params = (('fast', 12), ('slow', 26), ('signal', 9))

    def __init__(self):
        self.macd = bt.indicators.MACD(period_me1=self.p.fast, period_me2=self.p.slow, period_signal=self.p.signal)
        self.order_count = 0
        self.signal = None

    def next(self):
        if not self.position:
            if self.macd.macd > self.macd.signal:
                self.buy()
                self.order_count += 1
                self.signal = 1
        elif self.macd.macd < self.macd.signal:
            self.close()
            self.order_count += 1
            self.signal = 0
