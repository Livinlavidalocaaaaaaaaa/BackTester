import backtrader as bt

class BuyAndHold(bt.Strategy):
    def __init__(self):
        self.order = None
        self.bought = False
        self.signal = 0  # Initialize with 'no signal'
        self.order_count = 0

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()} {txt}')

    def start(self):
        self.val_start = self.broker.get_cash()  # keep the starting cash

    def next(self):
        if not self.bought:
            size = int(self.broker.get_cash() / self.data.close[0])
            self.order = self.buy(size=size)
            self.order_count += 1
            self.bought = True
            self.signal = 1  # Buy signal
            self.log(f'BUY CREATE, {self.data.close[0]:.2f}')
        else:
            self.signal = 0  # Hold signal

    def stop(self):
        # calculate the actual returns
        self.roi = (self.broker.get_value() / self.val_start) - 1.0
        print('ROI:        {:.2f}%'.format(100.0 * self.roi))