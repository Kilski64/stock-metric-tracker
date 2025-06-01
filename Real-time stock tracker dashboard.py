import yfinance as yf
from datetime import datetime
import pandas as pd
import os

tickers = ["NVDA", "TSLA", "GOOG", "INTC", "ARM"]
dat = yf.Tickers(" ".join(tickers))

all_data = [] # store each data for export

for symbol in tickers:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ticker_obj = dat.tickers[symbol]
        info = ticker_obj.info

        hist = ticker_obj.history(period="35d")
        if len(hist) >= 31:
            latest = hist["Close"].iloc[-1]
            return_1d = ((latest - hist["Close"].iloc[-2]) / hist["Close"].iloc[-2]) * 100
            return_7d = ((latest - hist["Close"].iloc[-6]) / hist["Close"].iloc[-6]) * 100
            return_30d = ((latest - hist["Close"].iloc[-31]) / hist["Close"].iloc[-31]) * 100
        else:
            return_1d = return_7d = return_30d = "Insufficient data"

        my_metrics = {
            "Ticker": symbol,
            "Timestamp": now,
            # stock price data
            "Current Price": info.get("currentPrice", "N/A"),
            "Open": info.get("open", "N/A"),
            "Close": info.get("previousClose", "N/A"),
            "Day Low": info.get("dayLow", "N/A"),
            "Day High": info.get("dayHigh", "N/A"),
            "52-Week High": info.get("fiftyTwoWeekHigh", "N/A"),
            "52-Week Low": info.get("fiftyTwoWeekLow", "N/A"),
            # volume
            "Volume": info.get("volume", "N/A"),
            "Avg. Volume": info.get("averageVolume", "N/A"),
            # returns
            "1-Day Return (%)": return_1d,
            "7-Day Return (%)": return_7d,
            "30-Day Return (%)": return_30d,
            # moving averages
            "50-Day MA": info.get("fiftyDayAverage", "N/A"),
            "200-Day MA": info.get("twoHundredDayAverage", "N/A"),
            # volatility
            "Beta": info.get("beta", "N/A"),
            # fundamentals
            "Market Cap": info.get("marketCap", "N/A"),
            "P/E Ratio (TTM)": info.get("trailingPE", "N/A"),
            "EPS (TTM)": info.get("trailingEps", "N/A"),
            "Dividend Yield": info.get("dividendYield", "N/A"),
            "Dividend Rate": info.get("dividendRate", "N/A")
        }
        all_data.append(my_metrics)

        print(f"\n===== {symbol} =====")
        for key, value in my_metrics.items():
            print(f"{key}: {value}")

# export to CSV
df = pd.DataFrame(all_data)
filename = r"C:\Users\user\Downloads\stock_metrics_summary.csv" # insert real filepath name
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", filename)
full_path = os.path.join(desktop_path, filename)
df.to_csv(full_path, mode='a', header=not os.path.exists(full_path), index=False)
print("\n✅ Data has been saved to 'stock_metrics_summary.csv'")

    


