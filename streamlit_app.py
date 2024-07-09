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

class RSIStrategy(bt.Strategy):
    params = (('period', 14), ('overbought', 70), ('oversold', 30))
    
    def __init__(self):
        self.rsi = bt.indicators.RSI(period=self.p.period)
        self.order_count = 0
        self.signal = None

    def next(self):
        if not self.position:
            if self.rsi < self.p.oversold:
                self.buy()
                self.order_count += 1
                self.signal = 1
        elif self.rsi > self.p.overbought:
            self.close()
            self.order_count += 1
            self.signal = 0

class MACDStrategy(bt.Strategy):
    params = (('fast', 12), ('slow', 26), ('signal', 9))
    
    def __init__(self):
        self.macd = bt.indicators.MACD(period_me1=self.p.fast, period_me2=self.p.slow, period_signal=self.p.signal)
        self.order_count = 0
        self.signal = None

    def next(self):
        if not self.position:
            if self.macd.macd > self.macd.signal:
                self.buy()
                self.order_count += 1
                self.signal = 1
        elif self.macd.macd < self.macd.signal:
            self.close()
            self.order_count += 1
            self.signal = 0

# Function to run backtest
def run_backtest(data, strategy_class, start_cash=10000.0, commission=0.001):
    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.addstrategy(strategy_class)
    cerebro.broker.setcash(start_cash)
    cerebro.broker.setcommission(commission=commission)
    strategies = cerebro.run()
    final_value = cerebro.broker.getvalue()
    strategy = strategies[0]
    trade_count = strategy.order_count
    current_signal = strategy.signal
    return final_value, trade_count, current_signal

# Function to run buy and hold
def buy_and_hold(data, start_cash=10000.0):
    initial_price = data.close[0]
    final_price = data.close[-1]
    shares = start_cash / initial_price
    final_value = shares * final_price
    return final_value

# Streamlit app
st.title('Dutch Stock Strategy Backtester')

# User inputs
start_cash = st.number_input('Starting Capital (EUR)', min_value=1000, value=10000, step=1000)
commission = st.number_input('Commission (fraction)', min_value=0.0, max_value=0.1, value=0.001, step=0.001, format="%.3f")

# Date range selection
end_date = st.date_input('End Date', value=datetime.now())
start_date = st.date_input('Start Date', value=end_date - timedelta(days=365))

results = []

for ticker, name in dutch_tickers.items():
    # Fetch data
    try:
        df = yf.download(ticker, start=start_date, end=end_date)
    except Exception as e:
        st.error(f"Failed to fetch data for {ticker}: {e}")
        continue

    if not df.empty:
        data = bt.feeds.PandasData(dataname=df)
        
        strategies = {
            'Moving Average Crossover': MovingAverageCrossover,
            'RSI': RSIStrategy,
            'MACD': MACDStrategy
        }
        
        for strat_name, strategy in strategies.items():
            final_value, trade_count, current_signal = run_backtest(data, strategy, start_cash, commission)
            profit = final_value - start_cash
            profit_percentage = (profit / start_cash) * 100

            buy_and_hold_value = buy_and_hold(df, start_cash)
            buy_and_hold_profit = buy_and_hold_value - start_cash
            diff_to_buy_and_hold = profit - buy_and_hold_profit

            close_date = df.index[-1].strftime('%Y-%m-%d')
            
            results.append({
                'Ticker': ticker,
                'Name': name,
                'Strategy': strat_name,
                'Final Value (EUR)': round(final_value, 2),
                'Profit (EUR)': round(profit, 2),
                'Profit (%)': round(profit_percentage, 2),
                'Close Date': close_date,
                'Trades': trade_count,
                'Difference to Buy & Hold (EUR)': round(diff_to_buy_and_hold, 2),
                'Buy/Sell Signal': current_signal
            })
    else:
        st.error(f"No data found for the ticker {ticker} within the selected date range.")

# Display results
results_df = pd.DataFrame(results)
st.table(results_df)

# Plot
cerebro = bt.Cerebro()
cerebro.adddata(data)
cerebro.addstrategy(MovingAverageCrossover)  # Using MA Crossover for plotting
cerebro.broker.setcash(start_cash)
cerebro.broker.setcommission(commission=commission)

# Run cerebro to generate plot data
cerebro.run()

# Plotting with Backtrader and saving the figure
fig = cerebro.plot(style='candlestick')[0][0]
buf = io.BytesIO()
fig.savefig(buf, format='png')
st.image(buf)
