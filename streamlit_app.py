import streamlit as st
import backtrader as bt
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import io
import matplotlib.pyplot as plt

# Define the list of tickers with their full names
dutch_tickers = {
    'ASML.AS': 'ASML Holding N.V.',
    'REN.AS': 'Relx PLC',
    'UNA.AS': 'Unilever PLC'
}

# Define strategies
class MovingAverageCrossover(bt.Strategy):
    params = (('fast', 20), ('slow', 50))
    
    def __init__(self):
        self.crossover = bt.indicators.CrossOver(bt.indicators.SMA(period=self.p.fast), 
                                                 bt.indicators.SMA(period=self.p.slow))

    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy()
        elif self.crossover < 0:
            self.close()

class RSIStrategy(bt.Strategy):
    params = (('period', 14), ('overbought', 70), ('oversold', 30))
    
    def __init__(self):
        self.rsi = bt.indicators.RSI(period=self.p.period)

    def next(self):
        if not self.position:
            if self.rsi < self.p.oversold:
                self.buy()
        elif self.rsi > self.p.overbought:
            self.close()

class MACDStrategy(bt.Strategy):
    params = (('fast', 12), ('slow', 26), ('signal', 9))
    
    def __init__(self):
        self.macd = bt.indicators.MACD(period_me1=self.p.fast, period_me2=self.p.slow, period_signal=self.p.signal)

    def next(self):
        if not self.position:
            if self.macd.macd > self.macd.signal:
                self.buy()
        elif self.macd.macd < self.macd.signal:
            self.close()

# Function to run backtest
def run_backtest(data, strategy, start_cash=10000.0, commission=0.001):
    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.addstrategy(strategy)
    cerebro.broker.setcash(start_cash)
    cerebro.broker.setcommission(commission=commission)
    cerebro.run()
    return cerebro.broker.getvalue()

# Streamlit app
st.title('Dutch Stock Strategy Backtester')

# User inputs
start_cash = st.number_input('Starting Capital (EUR)', min_value=1000, value=10000, step=1000)
commission = st.number_input('Commission (fraction)', min_value=0.0, max_value=0.1, value=0.001, step=0.001, format="%.3f")

# Ticker selection
selected_ticker = st.selectbox('Select Ticker', list(dutch_tickers.keys()), format_func=lambda x: f"{x} - {dutch_tickers[x]}")

# Date range
end_date = datetime.now()
start_date = end_date - timedelta(days=365)

# Fetch data
df = yf.download(selected_ticker, start=start_date, end=end_date)

if not df.empty:
    data = bt.feeds.PandasData(dataname=df)
    
    strategies = {
        'Moving Average Crossover': MovingAverageCrossover,
        'RSI': RSIStrategy,
        'MACD': MACDStrategy
    }
    
    results = []
    
    for name, strategy in strategies.items():
        final_value = run_backtest(data, strategy, start_cash, commission)
        profit = final_value - start_cash
        profit_percentage = (profit / start_cash) * 100
        results.append({
            'Strategy': name,
            'Final Value (EUR)': round(final_value, 2),
            'Profit (EUR)': round(profit, 2),
            'Profit (%)': round(profit_percentage, 2)
        })
    
    results_df = pd.DataFrame(results)
    st.table(results_df)
    
    # Plot
    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.addstrategy(MovingAverageCrossover)  # Using MA Crossover for plotting
    cerebro.broker.setcash(start_cash)
    cerebro.broker.setcommission(commission=commission)
    
    fig = plt.figure(figsize=(12, 8))
    cerebro.plot(fig=fig)
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    st.image(buf)
    
else:
    st.error("Failed to fetch data. Please try again.")
