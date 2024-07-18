import backtrader as bt

class FibonacciRetracementStrategy(bt.Strategy):
    params = (('period', 30),)

    def __init__(self):
        self.high_point = bt.indicators.Highest(self.data.high, period=self.p.period)
        self.low_point = bt.indicators.Lowest(self.data.low, period=self.p.period)
        self.fib_levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1]
        self.order_count = 0
        self.signal = None

    def next(self):
        range = self.high_point[0] - self.low_point[0]
        fib_values = [self.low_point[0] + level * range for level in self.fib_levels]

        if not self.position:
            if self.data.close[0] < fib_values[2]:  # Below 0.382 retracement
                self.buy()
                self.order_count += 1
                self.signal = 1
        else:
            if self.data.close[0] > fib_values[4]:  # Above 0.618 retracement
                self.sell()
                self.order_count += 1
                self.signal = 0