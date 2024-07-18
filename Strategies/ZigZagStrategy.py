import backtrader as bt
import numpy as np

class ZigZag(bt.Indicator):
    lines = ('zigzag',)
    params = (('depth', 5), ('deviation', 3))

    def __init__(self):
        self.peaks = []
        self.troughs = []
        self.trend = 1  # 1 for uptrend, -1 for downtrend
        self.last_extreme = 0

    def next(self):
        high, low = self.data.high[0], self.data.low[0]
        
        if len(self) <= self.p.depth:
            self.lines.zigzag[0] = 0
            return

        if self.trend == 1:
            if high > self.last_extreme:
                self.last_extreme = high
            elif low < self.last_extreme * (1 - self.p.deviation / 100):
                self.troughs.append((len(self) - 1, self.last_extreme))
                self.trend = -1
                self.last_extreme = low
        else:
            if low < self.last_extreme:
                self.last_extreme = low
            elif high > self.last_extreme * (1 + self.p.deviation / 100):
                self.peaks.append((len(self) - 1, self.last_extreme))
                self.trend = 1
                self.last_extreme = high

        if self.peaks or self.troughs:
            last_point = max(self.peaks + self.troughs)
            self.lines.zigzag[0] = last_point[1]
        else:
            self.lines.zigzag[0] = 0

class ZigZagStrategy(bt.Strategy):
    params = (('depth', 5), ('deviation', 3))

    def __init__(self):
        self.zigzag = ZigZag(self.data, depth=self.p.depth, deviation=self.p.deviation)
        self.order_count = 0
        self.signal = 0
        self.last_zigzag_value = None

    def next(self):
        current_zigzag = self.zigzag.zigzag[0]
        
        if current_zigzag != 0 and current_zigzag != self.last_zigzag_value:
            if self.last_zigzag_value is not None:
                if not self.position:
                    if current_zigzag > self.last_zigzag_value:  # Upward turn
                        self.buy()
                        self.order_count += 1
                        self.signal = 1
                elif current_zigzag < self.last_zigzag_value:  # Downward turn
                    self.sell()
                    self.order_count += 1
                    self.signal = -1
            self.last_zigzag_value = current_zigzag
        else:
            self.signal = 0