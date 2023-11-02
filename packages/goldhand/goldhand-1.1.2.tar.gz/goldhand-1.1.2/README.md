# Goldhand
The ultimate python package to work with stock and crypto data

```bash
pip install goldhand
```



# TradingView data


```python
from goldhand import *
# tradingView data
tw = Tw()

# get all the stocks data and store it into tw.stocks
tw.get_all_stock()

```



```python

# the data
print(tw.stocks.head())


```

          logoid  name     close    change  change_abs  Recommend.All    volume  \
    0      apple  AAPL  171.1400 -1.326107     -2.3000      -0.490909  30662438   
    1  microsoft  MSFT  339.5100  2.716849      8.9800       0.603030  35657067   
    2   alphabet  GOOG  126.5180 -9.707394    -13.6020      -0.424242  44507631   
    3     amazon  AMZN  121.1950 -5.728843     -7.3650      -0.490909  48906577   
    4     nvidia  NVDA  419.8826 -3.835605    -16.7474      -0.357576  24862603   
    
       Value.Traded  market_cap_basic  price_earnings_ttm  ...   type  subtype  \
    0  5.247570e+09      2.675643e+12           28.760608  ...  stock   common   
    1  1.210593e+10      2.522230e+12           32.878822  ...  stock   common   
    2  5.631016e+09      1.587213e+12           24.259937  ...  stock   common   
    3  5.927233e+09      1.243504e+12           96.377734  ...  stock   common   
    4  1.043937e+10      1.037110e+12          101.430718  ...  stock   common   
    
                 update_mode pricescale  minmov  fractional  minmove2     RSI[1]  \
    0  delayed_streaming_900        100       1       false         0  42.011543   
    1  delayed_streaming_900        100       1       false         0  54.436692   
    2  delayed_streaming_900        100       1       false         0  57.112393   
    3  delayed_streaming_900        100       1       false         0  46.987138   
    4  delayed_streaming_900        100       1       false         0  48.039037   
    
       currency  fundamental_currency_code  
    0       USD                        USD  
    1       USD                        USD  
    2       USD                        USD  
    3       USD                        USD  
    4       USD                        USD  
    
    [5 rows x 42 columns]



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

             date      open      high       low     close     volume  dividends  \
    0  2010-06-29  1.266667  1.666667  1.169333  1.592667  281494500        0.0   
    1  2010-06-30  1.719333  2.028000  1.553333  1.588667  257806500        0.0   
    2  2010-07-01  1.666667  1.728000  1.351333  1.464000  123282000        0.0   
    3  2010-07-02  1.533333  1.540000  1.247333  1.280000   77097000        0.0   
    4  2010-07-06  1.333333  1.333333  1.055333  1.074000  103003500        0.0   
    
       stock splits  rsi  sma_50  ...  sma_100  diff_sma100  sma_200  diff_sma200  \
    0           0.0  NaN     NaN  ...      NaN          NaN      NaN          NaN   
    1           0.0  NaN     NaN  ...      NaN          NaN      NaN          NaN   
    2           0.0  NaN     NaN  ...      NaN          NaN      NaN          NaN   
    3           0.0  NaN     NaN  ...      NaN          NaN      NaN          NaN   
    4           0.0  NaN     NaN  ...      NaN          NaN      NaN          NaN   
    
       bb_lower  bb_upper  diff_upper_bb  diff_lower_bb    local local_text  
    0       NaN       NaN            NaN            NaN                      
    1       NaN       NaN            NaN            NaN  maximum      $2.03  
    2       NaN       NaN            NaN            NaN                      
    3       NaN       NaN            NaN            NaN                      
    4  1.002387  1.797347      67.350706      -6.667877                      
    
    [5 rows x 21 columns]




# Helper functions



```python
!pip install pandas_ta
from datetime import datetime, timedelta
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
import plotly.express as px
from scipy.signal import argrelextrema
import numpy as np
import requests
import json


def get_base_stock_data(ticker):
    # Download historical stock data for the last year
    df = pd.DataFrame().ta.ticker(ticker).reset_index()
    df.columns = df.columns.str.lower()
    df['date']= [x.date() for x in df['date']]

    # Rsi
    df['rsi'] = ta.rsi(df['close'], 14)

    # SMAS
    df['sma_50']= ta.sma(df['close'], 50)
    df['diff_sma50'] = (df['close']/df['sma_50'] -1)*100
    df['sma_100']= ta.sma(df['close'], 100)
    df['diff_sma100'] = (df['close']/df['sma_100'] -1)*100
    df['sma_200']= ta.sma(df['close'], 200)
    df['diff_sma200'] = (df['close']/df['sma_200'] -1)*100

    #Bolinger bands
    bb = ta.bbands(df['close'])
    bb.columns = ['bb_lower', 'bb_mid', 'bb_upper', 'bandwidth', 'percent']
    df['bb_lower'] = bb['bb_lower']
    df['bb_upper'] = bb['bb_upper']
    df['diff_upper_bb'] = (df['bb_upper']/df['close'] -1)*100
    df['diff_lower_bb'] = (df['bb_lower']/df['close'] -1)*100
    return(df)

def add_locals_to_olhc(df):
    #local min maxs
    df['local'] = ''
    df['local_text'] = ''
    max_ids = list(argrelextrema(df['high'].values, np.greater, order=30)[0])
    min_ids = list(argrelextrema(df['low'].values, np.less, order=30)[0])
    df.loc[min_ids, 'local'] = 'minimum'
    df.loc[max_ids, 'local'] = 'maximum'


    states = df[df['local']!='']['local'].index.to_list()
    problem = []
    problem_list = []
    for i in range(0, (len(states)-1) ):

        if (df.loc[states[i], 'local'] != df.loc[states[i+1], 'local']):
            if (len(problem)==0):
                continue
            else:
                problem.append(states[i])
                text = df.loc[states[i], 'local']
                if(text=='minimum'):
                    real_min = df.loc[problem, 'low'].idxmin()
                    problem.remove(real_min)
                    df.loc[problem, 'local']=''
                else:
                    real_max = df.loc[problem, 'high'].idxmax()
                    problem.remove(real_max)
                    df.loc[problem, 'local']=''

                problem = []
        else:
            problem.append(states[i])

    states = df[df['local']!='']['local'].index.to_list()

    # if first is min ad the price
    if df.loc[states[0], 'local']== 'minimum':
        df.loc[states[0],'local_text'] = f"${round(df.loc[states[0], 'low'], 2)}"
    else:
        df.loc[states[0],'local_text'] = f"${round(df.loc[states[0], 'high'], 2)}"

    # add last fall if last local is max
    if list(df[df['local']!='']['local'])[-1]=='maximum':
        last_min_id = df.loc[df['low']==min(df['low'][-3:] )].index.to_list()[0]
        df.loc[last_min_id , 'local'] = 'minimum'

    states = df[df['local']!='']['local'].index.to_list()


    for i in range(1,len(states)):
        prev = df.loc[states[i-1], 'local']
        current= df.loc[states[i], 'local']
        prev_high = df.loc[states[i-1], 'high']
        prev_low = df.loc[states[i-1], 'low']
        current_high = df.loc[states[i], 'high']
        current_low = df.loc[states[i], 'low']
        if current == 'maximum':
            # rise
            rise = (current_high/ prev_low -1)*100
            if rise>100:
                df.loc[states[i], 'local_text'] = f'🚀🌌{round(((rise+100)/100), 2)}x<br>${round(current_high, 2)}'
            else:
                df.loc[states[i], 'local_text'] = f'🚀{round(rise, 2)}%<br>${round(current_high, 2)}'
        else:
            fall = round((1-(current_low / prev_high))*100, 2)
            df.loc[states[i], 'local_text'] = f'🔻{fall}%<br>${round(current_low, 2)}'
    return(df)

def plotly_last_year(df,plot_title, plot_height=900):
    tdf = df.tail(500)

    fig = go.Figure(data=go.Ohlc(x=tdf['date'], open=tdf['open'], high=tdf['high'], low=tdf['low'],close=tdf['close']))

    for index, row in tdf[tdf['local']!=''].iterrows():
        direction = row['local']
        tdate = row['date']
        local_text = row['local_text']
        min_price = row['low']
        max_price = row['high']
        if direction == 'maximum':
            fig.add_annotation( x=tdate, y=max_price, text=local_text, showarrow=True,
            align="center", bordercolor="#c7c7c7",
            font=dict(family="Courier New, monospace", size=16, color="#214e34" ), borderwidth=2,
            borderpad=4,
            bgcolor="#f4fdff",
            opacity=0.8,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            ax=-45,ay=-45)

        if direction == 'minimum':
            fig.add_annotation( x=tdate, y=min_price, text=local_text, showarrow=True,
            align="center", bordercolor="#c7c7c7",
            font=dict(family="Courier New, monospace", size=16, color="red" ), borderwidth=2,
            borderpad=4,
            bgcolor="#f4fdff",
            opacity=0.8,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            ax=45,ay=45)

        fig.update_layout(showlegend=False, plot_bgcolor='white', height=plot_height, title= plot_title)

    fig.update_xaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey'
    )
    fig.update_yaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey'
    )
    fig.update(layout_xaxis_rangeslider_visible=False)
    return(fig)


df = get_base_stock_data('TSLA')
df_with_locals = add_locals_to_olhc(df)
p = plotly_last_year(df_with_locals, 'Tesla')
p.show()
```


