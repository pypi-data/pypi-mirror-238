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
tw.get_sec_plot('AMD')

```
![Sector plot](img/sec_plot.png "Sector location of FDS")


```python
# Get a plot of the stock to see the location in the industry 
tw.get_sec_plot('AMD')

```
![Sector plot](img/ind_plot.png  "Sector location of FDS")



# Goldhand class


```python

# Get a detailed chart of a stock AMD
ticker = "AMD"
t = GoldHand(ticker)
t.df.tail().T
```
![data structure](img/df_structure.png "data structure")


```python

# Get a detailed chart of a stock AMD
ticker = "AMD"
t = GoldHand(ticker)
t.plotly_last_year(tw.get_plotly_title(ticker)).show()

```
!['Detailed stock chart'](img/stock_plot.png "Stock plot")

```python

# Get a detailed chart of a crypto
ticker = "BTC-USD"
t = GoldHand(ticker)
t.plotly_last_year(tw.get_plotly_title(ticker)).show()


```
!['Detailed crypto chart'](img/crypto_plot.png "crypto plot")




