import finplot as fplt
import yfinance as yf
import pandas as pd

# Downloaded historical data and saved to CSV. No need after running it once.
""" 
df = yf.download("AAPL", start="2020-01-01", end="2025-10-01", interval="1d")
df = df[["Open", "High", "Low", "Close", "Volume"]]
price_columns = ["Open", "High", "Low", "Close"]
df[price_columns] = df[price_columns].round(2)
df.to_csv("aapl.csv") 
"""

# Load data from CSV
stockData = pd.read_csv("aapl.csv", header=[0, 1])
stockData.drop(index=0, inplace=True)
stockData[('Unnamed: 0_level_0', 'Unnamed: 0_level_1')] = pd.to_datetime(stockData[('Unnamed: 0_level_0', 'Unnamed: 0_level_1')])
stockData.set_index(('Unnamed: 0_level_0', 'Unnamed: 0_level_1'), inplace=True)
stockData.index.name = None
print(stockData)

# Create a candlestick chart
fplt.candlestick_ochl(stockData[["Open", "Close", "High", "Low"]])
fplt.show()

