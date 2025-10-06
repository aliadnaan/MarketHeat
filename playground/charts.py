from operator import index
import finplot as fplt
import yfinance as yf
import pandas as pd

# Downloaded historical data and saved to CSV. No need after running it once.

# df = yf.download("AAPL", start="2020-01-01", end="2025-10-01", interval="1d")
# price_columns = ["Open", "High", "Low", "Close"]
# df[price_columns] = df[price_columns].round(2)
# df.to_csv("aapl.csv") 




data = yf.download("AAPL", period="1y", interval="1d", group_by="column")

if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)  # drop ticker layer

data = data[["Open", "High", "Low", "Close", "Volume"]]
data.reset_index().to_csv("aapl.csv", index=False)

# --- read whenever ----------------------------------------------------------
ohlc = (
    pd.read_csv("aapl.csv", parse_dates=["Date"])
      .set_index("Date")[["Open", "Close", "High", "Low"]]
      .astype("float64")
)

# optional: plot with finplot
fplt.candlestick_ochl(ohlc)
fplt.show()

