import requests
import json
import os
import datetime as dt
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from FinMind.data import DataLoader

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def dataset_generator_lstm(dataset, look_back=5):
    # A “lookback period” defines the window-size of how many
    # previous timesteps are used in order to predict
    # the subsequent timestep.
    dataX, dataY = [], []

    for i in range(len(dataset) - look_back):
        window_size_x = dataset[i:(i + look_back), :]
        dataX.append(window_size_x)
        dataY.append(dataset[i + look_back, 4])  # this is the label or actual y-value
    return np.array(dataX), np.array(dataY)


def Predict(Stock='2330'):

    # Get Data
    df = DataLoader().taiwan_stock_daily(
        stock_id=Stock,
        start_date=dt.date.today() - dt.timedelta(days=(10)),
        end_date=dt.date.today()
    )
    hist = df
    hist = hist.set_index('date')
    hist = hist.drop(['spread'], axis=1)
    hist = hist.drop(['Trading_money'], axis=1)
    hist = hist.drop(['Trading_turnover'], axis=1)
    hist = hist.drop(['stock_id'], axis=1)

    hist = hist.sort_index()
    print(hist.tail()['close'])
    # print(hist.info())
    time_stamp = hist.tail(1).index.item()
    time_stamp = dt.datetime.strptime(time_stamp, '%Y-%m-%d')

    old = hist.tail(1)['close'].values

    # print(hist.info())
    # Data Preprocess
    scaler_hist = MinMaxScaler(feature_range=(0, 1))
    scaled_hist = scaler_hist.fit_transform(hist)
    histX, histY = dataset_generator_lstm(scaled_hist)
    histX = np.reshape(histX, (histX.shape[0], histX.shape[1], 5))

    # Load Model
    checkpoint_path = './routers/Stock_model/' + Stock + '_model.hdf5'
    model_from_saved_checkpoint = load_model(checkpoint_path)

    print('\n')
    print('Predicting ' + Stock + ' price: ')

    # Predict
    testX_last_days = histX
    # print(histX.shape)
    predicted_forecast_price_test_x = 0
    predicted_forecast_price_test_x = model_from_saved_checkpoint.predict(testX_last_days)

    # print(predicted_forecast_price_test_x.shape)
    predicted_forecast_data = np.zeros((len(predicted_forecast_price_test_x), 5))
    predicted_forecast_data[0][4] = predicted_forecast_price_test_x

    forecast_price = scaler_hist.inverse_transform(predicted_forecast_data)[:, 4]

    index_list = time_stamp + dt.timedelta(hours=(1))

    result =  str(round(forecast_price[0], 2))
    # print(result)

    result_2 = ''

    new = round(forecast_price[0], 2)
    if(new > old):
        percent = float((new - old) / old)
        percent = percent * 100
        result_2 = '+' + str(round(percent, 4)) + '%'
        #print('預測會上漲' + str(round(percent, 4)) + '%')
    else:
        percent = float((old - new) / old)
        percent = percent * 100
        result_2 =  '-'  + str(round(percent, 4)) + '%'
        #print('預測會下跌' + str(round(percent, 4)) + '%')

    return result, result_2
