import backtrader as bt

class DonchianChannels(bt.Indicator):
    lines = ('upper', 'middle', 'lower')
    params = dict(period=20)

    def __init__(self):
        self.addminperiod(self.params.period)
        self.l.upper = bt.indicators.Highest(self.data.high, period=self.params.period)
        self.l.lower = bt.indicators.Lowest(self.data.low, period=self.params.period)
        self.l.middle = (self.l.upper + self.l.lower) / 2

class DonchianChannelStrategy(bt.Strategy):
    params = (('period', 20),)

    def __init__(self):
        self.donchian = DonchianChannels(period=self.p.period)
        self.order_count = 0
        self.signal = None

    def next(self):
        if not self.position:
            if self.data.close >= self.donchian.lines.upper:
                self.buy()
                self.order_count += 1
                self.signal = 1
        elif self.data.close <= self.donchian.lines.lower:
            self.close()
            self.order_count += 1
            self.signal = 0