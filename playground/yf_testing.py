import yfinance as yf

spy = yf.Ticker("SPY")
hist = spy.history(period="5d")

