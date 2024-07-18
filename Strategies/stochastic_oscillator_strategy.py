import backtrader as bt

class BollingerBandsStrategy(bt.Strategy):
    params = (('period', 20), ('devfactor', 2))

    def __init__(self):
        self.bband = bt.indicators.BollingerBands(period=self.p.period, devfactor=self.p.devfactor)
        self.order_count = 0
        self.signal = None

    def next(self):
        if not self.position:
            if self.data.close < self.bband.lines.bot:
                self.buy()
                self.order_count += 1
                self.signal = 1
        elif self.data.close > self.bband.lines.top:
            self.close()
            self.order_count += 1
            self.signal = 0