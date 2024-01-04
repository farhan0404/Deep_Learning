# -*- coding: utf-8 -*-
"""streamlit_app.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/104zAfQW2_j-GMj9eL1haoOQjm53fML1o
"""

#pip install streamlit

from datetime import date

import yfinance as yf

from plotly import graph_objs as go
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pylab
import scipy.stats as stats
import streamlit as st

START = "2004-09-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title('Stock Forecast App')

stocks = ('GOOG', 'AAPL', 'MSFT', 'GME')
selected_stock = st.selectbox('Select dataset for prediction', stocks)

@st.cache
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

data_load_state = st.text('Loading data...')
data = load_data(selected_stock)
data_load_state.text('Loading data... done!')

st.subheader('Raw data')
st.write(data.head())

def plot_raw_data(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
    fig.layout.update(title_text='FTSE STOCKS', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)


plot_raw_data(data)

def dataprocessing(data):
  data=norm(data)
  macd = MACD(data['Adj Close'], 12, 26, 9)
  macd.name = 'MACD'
  macd.tail()
  plt.figure(figsize=(21,7))
  plt.plot(macd,label='macd',color='red')
  plt.title('MACD')
  plt.legend(loc='upper left')
  st.pyplot()
  stochastics = stochastics_oscillator(data, 14)
  stochastics.name = 'Stochastics'
  stochastics.tail()
  plt.figure(figsize=(21,7))
  plt.plot(stochastics[-100:],label='Stochastics Oscillator',color='blue')
  plt.title('Stochastics Oscillator')
  plt.legend(loc='upper left')
  st.pyplot()
  atr = ATR(data,14)
  atr.rename(columns={0:'ATR'}, inplace=True)
  atr.tail()
  plt.figure(figsize=(21,7))
  plt.plot(atr[-100:],label='ATR',color='green')
  plt.title('Average True Range')
  plt.legend(loc='upper left')
  st.pyplot()
  data = pd.concat([data, macd, stochastics, atr], axis=1)
  data.drop([ 'H-L', 'H-PC', 'L-PC','Open','High','Low','Close'], axis=1 , inplace=True)
  data.tail()
  data['Y'] = data['Adj Close'].shift(-1)
  data.dropna(axis=0, inplace=True)
  data.head()
  data.set_index('Date', inplace=True)
  data.head()
  X, y = preprocess_df(data, shuffle=False)



  return X,y
#from tensorflow.keras.models import load_model
#loaded_model = load_model('my_model.keras')
from tensorflow.keras.models import load_model
import requests
from io import BytesIO

# Replace 'raw_model_url' with the raw URL of your model file on GitHub
raw_model_url = 'https://github.com/farhan0404/Deep_Learning/blob/main/my_model_2.keras'

response = requests.get(raw_model_url)
model_bytes = BytesIO(response.content)

loaded_model = load_model(model_bytes)

X,y = dataprocessing(data)
X_test_reshaped = X.reshape((X.shape[0], -1, X.shape[-1]))
test_predictions = loaded_model.predict(X_test_reshaped)

plt.figure(figsize=(10, 6))
plt.plot(dates[:len(y)], y, label='True Values', marker='o')
plt.plot(dates[:len(test_predictions)], test_predictions[:, 0], label='Predicted Values', marker='o')
plt.xlabel('Date')
plt.ylabel('Your Y Variable Name')
plt.title('True vs Predicted Values')
plt.legend()
st.pyplot()

pip show tensorflow

import sys
print(sys.version)