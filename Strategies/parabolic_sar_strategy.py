import backtrader as bt

class ParabolicSARStrategy(bt.Strategy):
    params = (('period', 2), ('af', 0.02), ('afmax', 0.2))

    def __init__(self):
        self.psar = bt.indicators.PSAR(period=self.p.period, af=self.p.af, afmax=self.p.afmax)
        self.order_count = 0
        self.signal = None

    def next(self):
        if not self.position:
            if self.data.close > self.psar:
                self.buy()
                self.order_count += 1
                self.signal = 1
        elif self.data.close < self.psar:
            self.close()
            self.order_count += 1
            self.signal = 0