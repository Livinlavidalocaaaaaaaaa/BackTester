import os
import importlib
import inspect
import backtrader as bt

# Path to the Strategies folder
STRATEGIES_PATH = './Strategies'

def load_strategies():
    strategies = {}
    for filename in os.listdir(STRATEGIES_PATH):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]  # Remove '.py'
            module = importlib.import_module(f'Strategies.{module_name}')
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, bt.Strategy) and obj != bt.Strategy:
                    strategies[name] = obj
    return strategies

# Load all strategies
all_strategies = load_strategies()

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
        
        for strat_name, strategy_class in all_strategies.items():
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
