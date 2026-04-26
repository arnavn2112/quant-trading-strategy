import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# Download stock data
stock = "AAPL"
data = yf.download(stock, start="2020-01-01", end="2023-01-01")

# Calculate moving averages
data['SMA_20'] = data['Close'].rolling(window=20).mean()
data['SMA_50'] = data['Close'].rolling(window=50).mean()

# Create signals
data['Signal'] = 0
data.loc[data['SMA_20'] > data['SMA_50'], 'Signal'] = 1
data.loc[data['SMA_20'] < data['SMA_50'], 'Signal'] = -1

# Strategy returns
data['Returns'] = data['Close'].pct_change()
data['Strategy_Returns'] = data['Returns'] * data['Signal'].shift(1)

# Cumulative performance
data['Cumulative_Market'] = (1 + data['Returns']).cumprod()
data['Cumulative_Strategy'] = (1 + data['Strategy_Returns']).cumprod()

# Plot results
plt.figure(figsize=(10,5))
plt.plot(data['Cumulative_Market'], label='Market')
plt.plot(data['Cumulative_Strategy'], label='Strategy')
plt.legend()
plt.title(f"{stock} Strategy vs Market")
plt.show()
