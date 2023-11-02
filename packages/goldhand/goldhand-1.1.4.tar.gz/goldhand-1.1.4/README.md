# Goldhand
The ultimate python package to work with stock and crypto data

```bash
pip install goldhand
```



# TradingView


```python
from goldhand import *

# tradingView data
tw = Tw()

# data frame of the stocks 
tw.stock

# data frame of the top 300 crypto currency
tw.crypto
```

```python
# Get a plot of the stock to see the location in the sector 
get_sec_plot()

```



```python

# the data
print(tw.stocks.head())


```


```python
# create a sector location plot
tw.get_sec_plot('FDS')

```

![Sector plot](img/sector_plot.png "Sector location of FDS")



```python
# create an industry location plot
tw.get_ind_plot('NIO')
```


# Stock data


```python

# Example usage replace with your desired stock ticker symbol
ticker = "TSLA"

t = GoldHand(ticker)
t.download_historical_data()
print(t.df.head())

p = t.plotly_last_year(tw.get_plotly_title(ticker))
p.show()
```


