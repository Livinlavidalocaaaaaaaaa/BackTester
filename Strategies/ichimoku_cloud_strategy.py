import backtrader as bt

class IchimokuCloudStrategy(bt.Strategy):
    params = (('tenkan', 9), ('kijun', 26), ('senkou', 52), ('chikou', 26))

    def __init__(self):
        self.ichimoku = bt.indicators.Ichimoku(tenkan=self.p.tenkan, kijun=self.p.kijun, 
                                               senkou=self.p.senkou, chikou=self.p.chikou)
        self.order_count = 0
        self.signal = None

    def next(self):
        if not self.position:
            if self.data.close > self.ichimoku.senkou_span_a and self.data.close > self.ichimoku.senkou_span_b:
                self.buy()
                self.order_count += 1
                self.signal = 1
        elif self.data.close < self.ichimoku.senkou_span_a and self.data.close < self.ichimoku.senkou_span_b:
            self.close()
            self.order_count += 1
            self.signal = 0