import yfinance as yf
from backend.supabase_client import supabase

def fetch_and_store(ticker="SPY", interval="1d", period="1y"):
    df = yf.download(ticker, period=period, interval=interval)

    if df is None or df.empty:
        return

    df = df[["Open", "High", "Low", "Close", "Volume"]].copy()
    df["timestamp"] = df.index.tz_localize("UTC") if df.index.tz is None else df.index.tz_convert("UTC")

    rows = [
        {
            "ticker": ticker,
            "interval": interval,
            "open": float(r.Open),
            "high": float(r.High),
            "low": float(r.Low),
            "close": float(r.Close),
            "volume": int(r.Volume),
            "timestamp": r.timestamp.to_pydatetime().isoformat(),
        }
        for r in df.itertuples(index=False)
    ]

    supabase.table("ohlc_data").insert(rows).execute()

if __name__ == "__main__":
    fetch_and_store("SPY", interval="1d", period="1y")
