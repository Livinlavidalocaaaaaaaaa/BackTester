import streamlit as st
import backtrader as bt
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import io
from Strategies.moving_average_crossover import MovingAverageCrossover
from Strategies.rsi_strategy import RSIStrategy
from Strategies.macd_strategy import MACDStrategy

# Define folder paths
TICKERS_CSV_PATH = './Tickers/tickers.csv'

# Read tickers from CSV
tickers_df = pd.read_csv(TICKERS_CSV_PATH)

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

# Function to run buy and hold
def buy_and_hold(data, start_cash=10000.0):
    initial_price = data['Close'].iloc[0]
    final_price = data['Close'].iloc[-1]
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
        
        for strat_name, strategy_class in [('MovingAverageCrossover', MovingAverageCrossover),
                                           ('RSIStrategy', RSIStrategy),
                                           ('MACDStrategy', MACDStrategy)]:
            final_value, trade_count, current_signal = run_backtest(data, strategy_class, start_cash, commission)
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
