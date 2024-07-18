import backtrader as bt

class SuperTrend(bt.Indicator):
    lines = ('supertrend',)
    params = (('period', 7), ('multiplier', 3))

    def __init__(self):
        self.atr = bt.indicators.ATR(self.data, period=self.p.period)
        self.h1 = (self.data.high + self.data.low) / 2
        self.h2 = bt.indicators.Highest(self.h1, period=self.p.period)
        self.l2 = bt.indicators.Lowest(self.h1, period=self.p.period)
        
    def next(self):
        up_band = self.h2[-1] + self.p.multiplier * self.atr[-1]
        dn_band = self.l2[-1] - self.p.multiplier * self.atr[-1]
        
        if self.data.close[-1] <= self.lines.supertrend[-1]:
            if self.data.close[0] > dn_band:
                self.lines.supertrend[0] = dn_band
            else:
                self.lines.supertrend[0] = self.lines.supertrend[-1]
        else:
            if self.data.close[0] < up_band:
                self.lines.supertrend[0] = up_band
            else:
                self.lines.supertrend[0] = self.lines.supertrend[-1]

class SupertrendStrategy(bt.Strategy):
    params = (('period', 7), ('multiplier', 3))

    def __init__(self):
        self.supertrend = SuperTrend(self.data, period=self.p.period, multiplier=self.p.multiplier)
        self.order_count = 0
        self.signal = 0

    def next(self):
        if not self.position:
            if self.data.close[0] > self.supertrend.supertrend[0]:
                self.buy()
                self.order_count += 1
                self.signal = 1
        elif self.data.close[0] < self.supertrend.supertrend[0]:
            self.sell()
            self.order_count += 1
            self.signal = -1
        else:
            self.signal = 0