import yfinance as yf
import pandas as pd

# Companies to fetch
tickers = ['AAPL', 'MSFT', 'TSLA', 'AMZN', 'GOOG']
data_list = []
company_id = 1

for ticker in tickers:
    print(f"Fetching data for {ticker}...")
    stock = yf.Ticker(ticker)
    
    try:
        # Get financials, balance sheet, and cash flow
        income = stock.financials
        balance = stock.balance_sheet
        cashflow = stock.cashflow
        
        # yfinance returns DataFrames where columns are dates (most recent first)
        # We need to flip it so period 1 is the oldest
        
        # Get common dates across all three
        dates = list(set(income.columns) & set(balance.columns) & set(cashflow.columns))
        dates.sort() # Oldest first
        
        period = 1
        for date in dates:
            # Safely get values, defaulting to 0 if not found
            def get_val(df, index_name, date_col):
                if index_name in df.index:
                    val = df.loc[index_name, date_col]
                    return float(val) if pd.notna(val) else 0.0
                return 0.0
            
            revenue = get_val(income, 'Total Revenue', date)
            net_income = get_val(income, 'Net Income', date)
            
            operating_cash_flow = get_val(cashflow, 'Operating Cash Flow', date)
            
            assets = get_val(balance, 'Total Assets', date)
            liabilities = get_val(balance, 'Total Liabilities Net Minority Interest', date)
            debt = get_val(balance, 'Total Debt', date)
            
            # Try different names for receivables
            receivables = get_val(balance, 'Accounts Receivable', date)
            if receivables == 0.0:
                receivables = get_val(balance, 'Net Receivables', date)
            
            # Basic sanity check to avoid completely empty periods
            if revenue > 0 and assets > 0:
                data_list.append({
                    'company_id': company_id,
                    'company_name': ticker,
                    'period': period,
                    'revenue': revenue,
                    'net_income': net_income,
                    'operating_cash_flow': operating_cash_flow,
                    'assets': assets,
                    'liabilities': liabilities,
                    'debt': debt,
                    'receivables': receivables
                })
                period += 1
                
        company_id += 1
    except Exception as e:
        print(f"Failed to fetch {ticker}: {e}")

df = pd.DataFrame(data_list)
df.to_csv('real_companies_data.csv', index=False)
print("Saved real_companies_data.csv!")
