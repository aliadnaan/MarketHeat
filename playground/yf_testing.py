from pathlib import Path
import os
from dotenv import load_dotenv
from supabase import create_client
import yfinance as yf
import pandas as pd

# Load Supabase credentials from playground-specific env file
load_dotenv(dotenv_path=Path(__file__).with_name(".env"))

supabase_url = os.getenv("SUPABASE_URL")
supabase_service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not supabase_url or not supabase_service_role_key:
	raise RuntimeError("Missing Supabase credentials in playground/.env")

supabase = create_client(supabase_url, supabase_service_role_key)

# Pick multiple tickers
tickers = ["SPY", "AAPL", "GOOGL"]

for ticker in tickers:
	df = yf.download(ticker, period="1mo", interval="1d").reset_index()

	# flatten possible multi-index columns from yfinance
	df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

	# convert dates to YYYY-MM-DD strings
	df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")

	# round the price columns to two decimals
	price_columns = ["Open", "High", "Low", "Close"]
	df[price_columns] = df[price_columns].round(2)

	for _, row in df.iterrows():
		supabase.table("ohlc_daily").upsert(
			{
				"ticker": ticker,
				"date": row["Date"],
				"open": float(row["Open"]),
				"high": float(row["High"]),
				"low": float(row["Low"]),
				"close": float(row["Close"]),
				"volume": int(row["Volume"]),
			}
		).execute()

