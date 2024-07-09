import streamlit as st
import backtrader as bt
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
import importlib.util

# Define folder paths
STRATEGIES_DIR = './Strategies/'
TICKERS_CSV_PATH = './Tickers/tickers.csv'

# Function to dynamically import all strategies from Strategies directory
def import_strategies():
    strategy_classes = {}
    for file_name in os.listdir(STRATEGIES_DIR):
        if file_name.endswith('.py'):
            module_name = file_name[:-3]  # Remove .py extension
            spec = importlib.util.spec_from_file_location(module_name, os.path.join(STRATEGIES_DIR, file_name))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            for name, obj in module.__dict__.items():
                if isinstance(obj, type) and issubclass(obj, bt.Strategy) and obj != bt.Strategy:
                    strategy_classes[name] = obj
    return strategy_classes

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
    trade_count = strategy.order_count if hasattr(strategy, 'order_count') else 0
    current_signal = strategy.signal if hasattr(strategy, 'signal') else None
    return final_value, trade_count, current_signal

# Streamlit app
st.title('Dutch Stock Strategy Backtester')

# User inputs
start_cash = st.number_input('Starting Capital (EUR)', min_value=1000, value=10000, step=1000)
commission = st.number_input('Commission (fraction)', min_value=0.0, max_value=0.1, value=0.001, step=0.001, format="%.3f")

# Date range selection
end_date = st.date_input('End Date', value=datetime.now())
start_date = st.date_input('Start Date', value=end_date - timedelta(days=365))

# Import all strategies dynamically
strategies = import_strategies()

# Read tickers from CSV
tickers_df = pd.read_csv(TICKERS_CSV_PATH)

results = []

for index, row in tickers_df.iterrows():
    ticker = row['Ticker']
    name = row['Name']
    
    # Fetch data
    try:
        df = yf.download(ticker, start=start_date, end=end_date)
    except Exception as e:
        st.error(f"Failed to fetch data for {ticker}: {e}")
        continue

    if not df.empty:
        data = bt.feeds.PandasData(dataname=df)
        
        for strategy_name, strategy_class in strategies.items():
            final_value, trade_count, current_signal = run_backtest(data, strategy_class, start_cash, commission)
            profit = final_value - start_cash
            profit_percentage = (profit / start_cash) * 100

            close_date = df.index[-1].strftime('%Y-%m-%d')
            
            results.append({
                'Ticker': ticker,
                'Name': name,
                'Strategy': strategy_name,
                'Final Value (EUR)': round(final_value, 2),
                'Profit (EUR)': round(profit, 2),
                'Profit (%)': round(profit_percentage, 2),
                'Close Date': close_date,
                'Trades': trade_count,
                'Buy/Sell Signal': current_signal
            })
    else:
        st.error(f"No data found for the ticker {ticker} within the selected date range.")

# Display results
results_df = pd.DataFrame(results)
st.table(results_df)
