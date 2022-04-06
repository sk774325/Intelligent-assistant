import re
from fastapi import APIRouter
from database import SESSION
from database import Stock, database_Stock, Favorite, database_Favorite
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import datetime as datetime
import talib
import requests
from io import StringIO
from bs4 import BeautifulSoup
from backtesting import Backtest, Strategy 
from backtesting.lib import crossover
from backtesting.test import SMA, GOOG

router = APIRouter()
start = datetime.utcnow()
time_start = start

@router.get("/stock_inter")
async def basic(id: int):
    # 爬蟲
    try:
        days = 24 * 60 * 60    #一天有86400秒 
        initial = datetime.datetime.strptime( '1970-01-01' , '%Y-%m-%d' )
        start = datetime.datetime.strptime( str(time_start) , '%Y-%m-%d' )
        time_end = '2022-01-01'
        end = datetime.datetime.strptime( str(time_end), '%Y-%m-%d' )
        period1 = start - initial
        period2 = end - initial
        s1 = period1.days * days
        s2 = period2.days * days
        url ="https://query1.finance.yahoo.com/v7/finance/download/"+id+".TW?period1="+str(s1)+"&period2="+str(s2)+"&interval=1d&events=history&includeAdjustedClose=true" 
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36"}
        response = requests.get(url,headers = headers)
        response.text
        df = pd.read_csv(StringIO(response.text),index_col = "Date",parse_dates = ["Date"])
        write_data(df,response,id)
    except:
        print("輸入錯誤格式，請重新輸入")
    # plot
    address = r"..\stock\\" + id + ".csv"
    df_kd_draw = pd.read(address)
    df_kd_draw['K'], df_kd_draw['D'] = talib.STOCH(df_kd_draw['High'], 
                                         df_kd_draw['Low'], 
                                         df_kd_draw['Close'], 
                                         fastk_period=9,
                                         slowk_period=3,
                                         slowk_matype=1,
                                         slowd_period=3,
                                         slowd_matype=1)
    add_plot =[mpf.make_addplot(df_kd_draw["K"],panel= 2,color="b"),
    mpf.make_addplot(df_kd_draw["D"],panel= 2,color="r")]
    mc = mpf.make_marketcolors(up='r', down='g', inherit=True)
    s  = mpf.make_mpf_style(base_mpf_style='yahoo', marketcolors=mc)
    address = r"..\images\\" + id + "_kd_ptr" + ".png" #自己改路徑
    kwargs = dict(type='candle', mav=(5,10,20,60), volume = True,figsize=(20, 10),title = id+" KD picture", style=s,addplot=add_plot)
    mpf.plot(df_kd_draw, **kwargs, savefig=address)
    re_address = "http://127.0.0.1:8000//images/" + id + "_kd_ptr.png"
    return re_address

def write_data(data_frame,response,id):
    data_frame = pd.read_csv(StringIO(response.text),index_col = "Date",parse_dates = ["Date"])
    data_frame
    address = r"..\stock\\" + id + ".csv" #自己改路徑
    data_frame.to_csv(address)

### image plot 
###
###
@router.get("/macd_draw")
async def MACD_draw(id: int):
#Calculate the MACD and Signal line indicators
#Calculate the short term exponential moving average (EMA)
#指數移動平均線
    address = r"..\stock\\" + id + ".csv"
    data_frame = pd.read(address)
    ShortEMA=data_frame.Close.ewm(span=12,adjust=False).mean()
#Calculate the long term exponential moving average (EMA)
    LongEMA=data_frame.Close.ewm(span=26,adjust=False).mean()
#Calculat the MACD line
    MACD=ShortEMA-LongEMA
#Calculat the Signal line
    signal=MACD.ewm(span=9,adjust=False).mean()
    data_frame['MACD'] = MACD
    data_frame['Signal'] = signal
    add_plot =[mpf.make_addplot(data_frame["MACD"],panel= 2,color="b"),
    mpf.make_addplot(data_frame["Signal"],panel= 2,color="r")]
    mc = mpf.make_marketcolors(up='r', down='g', inherit=True)
    s  = mpf.make_mpf_style(base_mpf_style='yahoo', marketcolors=mc)
    kwargs = dict(type='candle', mav=(5,10,20,60), volume = True,figsize=(20, 10),title = id+" MACD", style=s,addplot=add_plot)
    address = r"..\images\\" + id + "_MACD_ptr" + ".png" #自己改路徑
    mpf.plot(data_frame, **kwargs, savefig=address)
    re_address = "http://127.0.0.1:8000/images/" + id + "_MACD_ptr.png"
    return re_address

# @router.get("/kd")
# async def KD_draw(id: int):
#     address = r"..\stock\\" + id + ".csv"
#     df_kd_draw = pd.read(address)
#     df_kd_draw['K'], df_kd_draw['D'] = talib.STOCH(df_kd_draw['High'], 
#                                          df_kd_draw['Low'], 
#                                          df_kd_draw['Close'], 
#                                          fastk_period=9,
#                                          slowk_period=3,
#                                          slowk_matype=1,
#                                          slowd_period=3,
#                                          slowd_matype=1)
#     add_plot =[mpf.make_addplot(df_kd_draw["K"],panel= 2,color="b"),
#     mpf.make_addplot(df_kd_draw["D"],panel= 2,color="r")]
#     mc = mpf.make_marketcolors(up='r', down='g', inherit=True)
#     s  = mpf.make_mpf_style(base_mpf_style='yahoo', marketcolors=mc)
#     address = r"..\images\\" + id + "_kd_ptr" + ".png" #自己改路徑
#     kwargs = dict(type='candle', mav=(5,10,20,60), volume = True,figsize=(20, 10),title = id+" KD picture", style=s,addplot=add_plot)
#     mpf.plot(df_kd_draw, **kwargs, savefig=address)
#     re_address = "http://127.0.0.1:8000/images/" + id + "_kd_ptr.png"
#     return re_address

@router.get("/kd_golden")
async def KD_golden(id: int):
    ##############KD死亡交叉回測
    address = r"..\stock\\" + id + ".csv"
    df_kd_skill = pd.read(address)
    df_kd_skill = df_kd_skill.loc[time_start:]
    #print(df_kd_skill)
    np.any(pd.isnull(df_kd_skill))
    df_kd_skill['K'], df_kd_skill['D'] = talib.STOCH(df_kd_skill['High'], 
                                            df_kd_skill['Low'], 
                                            df_kd_skill['Close'], 
                                            fastk_period=9,
                                            slowk_period=3,
                                            slowk_matype=1,
                                            slowd_period=3,
                                            slowd_matype=1)


    df_kd_skill["B_K"] = df_kd_skill["K"].shift(1)
    df_kd_skill["B_D"] = df_kd_skill["D"].shift(1)
    df_kd_skill.tail()
    #   KD黃金交叉的那天標記為1，沒有的標記為0
    buy = []
    for i in range(len(df_kd_skill)):
        if df_kd_skill["B_K"][i] <  df_kd_skill["B_D"][i] and df_kd_skill["K"][i] > df_kd_skill["D"][i]:
            buy.append(1)
        else:
            buy.append(0)
    df_kd_skill["buy"] = buy

    #df_kd_skill.loc[df_kd_skill["buy"].isin(["1"])]

    #有買進當然就要有賣出，那賣出的點我們就是利用KD死亡交叉，步驟跟買進類似，這次我們建立一個sell的空格，並將死亡交叉的那天標記為-1，沒有的標記為0
    sell = []
    for i in range(len(df_kd_skill)):
        if df_kd_skill["B_K"][i] > df_kd_skill["B_D"][i] and df_kd_skill["K"][i]< df_kd_skill["D"][i]:
            sell.append(-1)
        else:
            sell.append(0)
    df_kd_skill["sell"] = sell
    #透過loc，並使用isin將sell中-1的值列出，確認K值是否從大於D值變成小於D值    
    #df_kd_skill.loc[df_kd_skill["sell"].isin(["-1"])]

    #進出場點可視化
    #buy
    buy_mark = []
    for i in range(len(df_kd_skill)):
        if df_kd_skill["buy"][i] == 1:
            buy_mark.append(df_kd_skill["High"][i] + 10)
        else:
            buy_mark.append(np.nan)
    df_kd_skill["buy_mark"] = buy_mark
    #sell
    sell_mark = []
    for i in range(len(df_kd_skill)):
        if df_kd_skill["sell"][i] == -1:
            sell_mark.append(df_kd_skill["Low"][i] - 10)
        else:
            sell_mark.append(np.nan)
    df_kd_skill["sell_mark"] = sell_mark
    #綠色是賣出 紅色是買
    df_kd_skill.index  = pd.DatetimeIndex(df_kd_skill.index)
    mc = mpf.make_marketcolors(up='r', down='g', inherit=True)
    s  = mpf.make_mpf_style(base_mpf_style='yahoo', marketcolors=mc)
    add_plot =[mpf.make_addplot(df_kd_skill["buy_mark"],scatter=True, markersize=100, marker='v', color='r'),
            mpf.make_addplot(df_kd_skill["sell_mark"],scatter=True, markersize=100, marker='^', color='g'),
            mpf.make_addplot(df_kd_skill["K"],panel= 2,color="b"),
            mpf.make_addplot(df_kd_skill["D"],panel= 2,color="r")]
    kwargs = dict(type='candle', volume = True,figsize=(20, 10),title = id+"KDoperation", style=s,addplot=add_plot)
    address = r"..\images\\" + id + "_kd_operation" + ".png" 
    mpf.plot(df_kd_skill, **kwargs, savefile=address)
    re_address = "http://127.0.0.1:8000/images/" + id + "_kd_operation.png"
    return re_address
# create a funtion to signal when to buy and sell an asset
#買賣點的判斷，這只是一個示範，並不能實際用於買賣股票!!!

def MACD_Buy_Sell(signal):
    Buy=[]
    Sell=[]
    flag=-1
    for i in range(0,len(signal)):
        if signal['MACD'][i] > signal['Signal'][i]:
            Sell.append(np.nan)
            if flag !=1:
                Buy.append(signal['Close'][i])
                flag=1
            else:
                Buy.append(np.nan)
        elif signal['MACD'][i] < signal['Signal'][i]:
            Buy.append(np.nan)
            if flag !=0:
                Sell.append(signal['Close'][i])
                flag=0
            else:
                Sell.append(np.nan)
        else:
            Buy.append(np.nan)
            Sell.append(np.nan)
    return(Buy,Sell)

@router.get("/macd_op")
async def MACD_OP(id: int):
    address = r"..\stock\\" + id + ".csv"
    df = pd.read(address)

    a=MACD_Buy_Sell(df)
    df['Buy_Signal_Price']=a[0]
    df['Sell_Signal_Price']=a[1]
    address = r"..\images\\" + id + "MACD_operation" + ".csv" #自己改路徑
    df.to_csv(address)
    #Visually show the stock buy and sell signal
    plt.figure(figsize=(12.2,4.5))
    # ^ = shift + 6
    plt.scatter(df.index,df['Buy_Signal_Price'],color='red', label='Buy',marker='^',alpha=1)
    #小寫的v
    plt.scatter(df.index,df['Sell_Signal_Price'],color='green', label='Sell',marker='v',alpha=1)
    plt.plot(df['Close'], label='Close Price', alpha=0.35)
    plt.title('MACD operation')
    #字斜45度角
    plt.xticks(rotation=45)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend(loc='upper left')
    plt.show()
    address = r"..\images\\" + id + "_MACD_OP.png"
    plt.savefig(address)
    re_address = "http://127.0.0.1:8000/images/" + id + "_MACD_OP.png"
    return re_address

@router.get("/boolean")
async def boolean_draw(id: int):
#boolean
#timeperiod : 為均線週期，通常我會使用20
#nbdevup、nbdevdn : 為上下的標準差，這裡我會用我習慣的2.0倍標準差
#matype : 一樣是平滑的種類，這裡我們就不變動
    address = r"..\stock\\" + id + ".csv"
    df_boolean_draw = pd.read(address)
    df_boolean_draw["upper"],df_boolean_draw["middle"],df_boolean_draw["lower"] = talib.BBANDS(df_boolean_draw["Close"], timeperiod=20, nbdevup=2.0, nbdevdn=2.0, matype=0)

    add_plot =[mpf.make_addplot(df_boolean_draw[['upper','lower']],linestyle='dashdot'),
            mpf.make_addplot(df_boolean_draw['middle'],linestyle='dotted',color='y'),
            ]
    mc = mpf.make_marketcolors(up='r', down='g', inherit=True)
    s  = mpf.make_mpf_style(base_mpf_style='yahoo', marketcolors=mc)
    kwargs = dict(type='candle', volume = True,figsize=(20, 10),title = id+"boolean", style=s,addplot=add_plot)
    #print("this is 布林通道")
    address = r"..\images\\" + id + "_booleanPath_ptrs" + ".png" #自己改路徑
    mpf.plot(df_boolean_draw, **kwargs, savefile=address)
    re_address = "http://127.0.0.1:8000/images/" + id + "_booleanPath_ptrs.png"
    return re_address
