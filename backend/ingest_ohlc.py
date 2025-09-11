import yfinance as yf
from supabase_client import supabase
import datetime

def fetch_and_store(ticker="SPY", interval="1d", period="1y"):
	data = yf.download(ticker, period=period, interval=interval)

	for index, row in data.iterrows():
		entry = {
			"ticker": ticker,
			"interval": interval,
			"open": float(row["Open"]),
			"high": float(row["High"]),
			"low": float(row["Low"]),
			"close": float(row["Close"]),
			"volume": int(row["Volume"]),
			"timestamp": index.to_pydatetime().isoformat()
		}
		supabase.table("ohlc_data").insert(entry).execute()

if __name__ == "__main__":
	fetch_and_store("SPY")
