import streamlit as st 
import pandas as pd
import numpy as np
import ccxt
import pandas_ta as ta
import matplotlib.pyplot as plt



# define exchange
exchange = ccxt.bybit()


# needed functions for useability

def get_ticker_list():
            
             

             sf = exchange.fetch_markets()   
             a= len(sf)
             word = 'USDT'
             l = []
             for i in range(0,a):
                    if word in sf[i]['symbol']: 
                        l.append(sf[i]['symbol']) 
             return(l)

def get_data(asset,time,exchange):
    bars = exchange.fetch_ohlcv(asset, timeframe=time, limit=10000)
    df = pd.DataFrame(bars, columns=['time','open','high','low','close','volume'])
    df['time'] = pd.to_datetime(df['time'], unit=('ms'))
    return(df)
    
def rsi(data):
    l =  ta.rsi(data,length = 14)
    return(l)
    
def ma(data):
    l = ta.sma(data,200)
    t = ta.sma(data,50)
    l = t[len(t)-1]/l[len(l)-1]
    return(l)

def macd(data):
    l = ta.macd(data, fast=12, slow=26, append=True)
    l = l["MACD_12_26_9"][len(l)-1]/l["MACDs_12_26_9"][len(l)-1]
    l = round(l,3)
    return(l)

def custom_ma(data,length):
    l = ta.sma(data,length)
    return(l)
# get all avaiable Ticker from Binance

ticker  = get_ticker_list()









st.set_page_config(page_title = 'Crypto Dashboard', 
    layout='wide',
    page_icon='⚡️')
    
    
    
    
    
    
# optionsbar to select Ticker from Binance

ticker_option = st.sidebar.selectbox('Wähle deinen Ticker', (ticker ))

time_option = st.sidebar.selectbox('Wähle den Timeframe', ("1m","5m","15m","1h","4h","1d","1w" ))

dataframe = 0

uploaded_file = st.sidebar.file_uploader("Lade eine Datei hoch")

if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(uploaded_file, sep=",")
    dataframe.index = pd.to_datetime(dataframe.DateTime)

###
### GET DATAFRAME FROM INPUT
###

df = get_data(ticker_option,time_option,exchange)
df.index = pd.to_datetime(df.time)

# Calculate RSI
rsi_value = rsi(df.close)
rsi_value = round(rsi_value[len(rsi_value)-1],2)

# Calculate MA

ma_ratio = ma(df.close) 
ma_ratio  = round(ma_ratio ,4)

# calculate MACD

macd_ratio = macd(df.close)


### top row 

st.markdown(f"<h1 style='text-align: center;'>{ticker_option} {time_option} - Technische Indikatoren\n</h1>", unsafe_allow_html=True)

first_kpi, second_kpi, third_kpi = st.columns(3)


with first_kpi:
    st.markdown(f"<h1 style='text-align: center; color: white;'>RSI</h1>", unsafe_allow_html=True)
    if rsi_value > 50:
        st.markdown(f"<h1 style='text-align: center; color: lightgreen;'>{rsi_value}</h1>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h1 style='text-align: center; color: red;'>{rsi_value}</h1>", unsafe_allow_html=True)

with second_kpi:
    st.markdown(f"<h1 style='text-align: center; color: white;'>MA Ratio</h1>", unsafe_allow_html=True)
    if ma_ratio > 1:
        st.markdown(f"<h1 style='text-align: center; color: lightgreen;'>{ma_ratio }</h1>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h1 style='text-align: center; color: red;'>{ma_ratio }</h1>", unsafe_allow_html=True)
        
with third_kpi:
    st.markdown(f"<h1 style='text-align: center; color: white;'>MACD Signal</h1>", unsafe_allow_html=True)
    if macd_ratio > 1:
        st.markdown(f"<h1 style='text-align: center; color: lightgreen;'>{macd_ratio}</h1>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h1 style='text-align: center; color: red;'>{macd_ratio}</h1>", unsafe_allow_html=True)


### second row 

st.markdown("<hr/>", unsafe_allow_html=True)

st.markdown("## Performance Indikatoren")

first_kpi, second_kpi, third_kpi, fourth_kpi, fifth_kpi, sixth_kpi = st.columns(6)


with first_kpi:
    st.markdown("**First KPI**")
    number1 = 111 
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number1}</h1>", unsafe_allow_html=True)

with second_kpi:
    st.markdown("**Second KPI**")
    number2 = 222 
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number2}</h1>", unsafe_allow_html=True)

with third_kpi:
    st.markdown("**Third KPI**")
    number3 = 333 
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number3}</h1>", unsafe_allow_html=True)

with fourth_kpi:
    st.markdown("**First KPI**")
    number1 = 111 
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number1}</h1>", unsafe_allow_html=True)

with fifth_kpi:
    st.markdown("**Second KPI**")
    number2 = 222 
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number2}</h1>", unsafe_allow_html=True)

with sixth_kpi:
    st.markdown("**Third KPI**")
    number3 = 333 
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number3}</h1>", unsafe_allow_html=True)

st.markdown("<hr/>", unsafe_allow_html=True)


st.markdown("## Market Daten: Charts")

first_chart, second_chart = st.columns(2)


with first_chart:
    ma_length = st.number_input("Moving Average Länge", min_value=1, max_value=200, label_visibility="visible")
    df["200 MA"] = custom_ma(df.close,ma_length)
    
    chart_data = pd.DataFrame(df,columns=["close","200 MA"])

    st.line_chart(chart_data)
    

with second_chart:
    if type(dataframe) != int:
        chart_data = pd.DataFrame(dataframe,columns=['Value'])
        st.line_chart(chart_data)
        
    else:
        ma_length1 = st.number_input("Volume Moving Average Länge", min_value=1, max_value=200, label_visibility="visible")
        df["VMA"] = custom_ma(df.volume,ma_length1)
        chart_data = pd.DataFrame(df, columns=["volume","VMA"])
        st.line_chart(chart_data)


st.markdown("## Chart Section: 2")

first_chart, second_chart = st.columns(2)


with first_chart:
    chart_data = pd.DataFrame(np.random.randn(100, 3),columns=['a', 'b', 'c'])
    st.line_chart(chart_data)

with second_chart:
    chart_data = pd.DataFrame(np.random.randn(2000, 3),columns=['a', 'b', 'c'])
    st.line_chart(chart_data)
