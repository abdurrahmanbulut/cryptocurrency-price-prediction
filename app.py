from flask import Flask, render_template, request, session, redirect, url_for
from functools import wraps
import time
from flask import jsonify
from flask import Flask
import requests
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta




app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')



@app.route("/predict", methods=["POST"])
def predict():
    coin = str(request.form.get('coin') or "")
    coin = coin.upper()
    hours = int(request.form.get('hour'))
    print("deneme")
    print(coin)
    print(hours)
    # Get the coin data from Binance
    symbol = coin + 'USDT'
    interval = '1h'
    limit = 1000
    response = requests.get(f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}')
    data = response.json()
    df = pd.DataFrame(data)
    df = df.iloc[:, :6]
    df.columns = ['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']
    df['Datetime'] = pd.to_datetime(df['Datetime'], unit='ms')
    df['Close'] = df['Close'].astype(float)

    # Create rolling mean and standard deviation columns
    rolling_window_hours = 24
    rolling_mean = df['Close'].rolling(window=rolling_window_hours).mean()
    rolling_std = df['Close'].rolling(window=rolling_window_hours).std()
    df['RollingMean'] = rolling_mean
    df['RollingStd'] = rolling_std

    # Create the input features and target variable
    look_ahead_hours = hours
    X = df[['RollingMean', 'RollingStd']].values[:-look_ahead_hours]
    y = df['Close'].values[look_ahead_hours:]

    from sklearn.impute import SimpleImputer

    # create an imputer object with mean strategy
    imputer = SimpleImputer(strategy='mean')

    # impute missing values in X
    X = imputer.fit_transform(X)

    # Split the data into training and testing sets
    test_size = 0.2
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, shuffle=True)

    # Train the linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predict the next hour's closing price
    last_hour_data = df[['RollingMean', 'RollingStd']].iloc[-1].values.reshape(1, -1)
    next_hour_price = model.predict(last_hour_data)[0]

    last_hour_price = df['Close'].iloc[-1]
    return render_template('index.html', price=next_hour_price, timee=look_ahead_hours, coin=coin)
    


if __name__ == '__main__':
    app.debug = True
    app.run()
