import backtrader as bt

class KeltnerChannel(bt.Indicator):
    lines = ('mid', 'top', 'bot')
    params = (('period', 20), ('devfactor', 2),)

    def __init__(self):
        self.ema = bt.indicators.EMA(self.data.close, period=self.p.period)
        self.atr = bt.indicators.ATR(self.data, period=self.p.period)
        self.lines.mid = self.ema
        self.lines.top = self.ema + self.atr * self.p.devfactor
        self.lines.bot = self.ema - self.atr * self.p.devfactor

class KeltnerChannelStrategy(bt.Strategy):
    params = (('period', 20), ('devfactor', 2))

    def __init__(self):
        self.kc = KeltnerChannel(self.data, period=self.p.period, devfactor=self.p.devfactor)
        self.order_count = 0
        self.signal = 0

    def next(self):
        if not self.position:
            if self.data.close > self.kc.top[0]:
                self.buy()
                self.order_count += 1
                self.signal = 1
        elif self.data.close < self.kc.bot[0]:
            self.sell()
            self.order_count += 1
            self.signal = -1
        else:
            self.signal = 0