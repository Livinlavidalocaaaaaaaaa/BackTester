import backtrader as bt

class MovingAverageCrossover(bt.Strategy):
    params = (('fast', 20), ('slow', 50))

    def __init__(self):
        self.crossover = bt.indicators.CrossOver(bt.indicators.SMA(period=self.p.fast),
                                                 bt.indicators.SMA(period=self.p.slow))
        self.order_count = 0
        self.signal = None

    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy()
                self.order_count += 1
                self.signal = 1
        elif self.crossover < 0:
            self.close()
            self.order_count += 1
            self.signal = 0
