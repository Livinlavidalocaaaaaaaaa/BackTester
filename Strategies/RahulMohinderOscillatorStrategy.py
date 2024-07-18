import backtrader as bt

class RahulMohinderOscillatorStrategy(bt.Strategy):
    params = (
        ('fast_ema', 5),
        ('slow_ema', 20),
        ('signal_ema', 5),
        ('atr_period', 14),
        ('atr_multiplier', 2),
    )

    def __init__(self):
        # Calculate EMAs
        self.fast_ema = bt.indicators.EMA(self.data.close, period=self.p.fast_ema)
        self.slow_ema = bt.indicators.EMA(self.data.close, period=self.p.slow_ema)
        
        # Calculate Momentum
        self.momentum = self.fast_ema - self.slow_ema
        
        # Calculate Signal Line
        self.signal_line = bt.indicators.EMA(self.momentum, period=self.p.signal_ema)
        
        # Calculate ATR
        self.atr = bt.indicators.ATR(self.data, period=self.p.atr_period)
        
        # Calculate Trigger Lines
        self.upper_trigger = self.signal_line + self.p.atr_multiplier * self.atr
        self.lower_trigger = self.signal_line - self.p.atr_multiplier * self.atr
        
        # Crossover indicators
        self.crossover_signal = bt.indicators.CrossOver(self.momentum, self.signal_line)
        self.crossover_upper = bt.indicators.CrossOver(self.momentum, self.upper_trigger)
        self.crossover_lower = bt.indicators.CrossOver(self.momentum, self.lower_trigger)
        
        self.order_count = 0
        self.signal = None

    def next(self):
        if not self.position:
            if self.crossover_signal > 0 or self.crossover_upper > 0:
                self.buy()
                self.order_count += 1
                self.signal = 1
        else:
            if self.crossover_signal < 0 or self.crossover_lower < 0:
                self.sell()
                self.order_count += 1
                self.signal = 0