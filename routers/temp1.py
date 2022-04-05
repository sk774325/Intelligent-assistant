
while True:
    try:
        days = 24 * 60 * 60    #一天有86400秒 
        stock_id = input("請輸入股票代碼 : ",)
        time_start = input("輸入開始日期 : ")
        time_end = input("輸入結束日期 : ")
        initial = datetime.datetime.strptime( '1970-01-01' , '%Y-%m-%d' )
        start = datetime.datetime.strptime( str(time_start) , '%Y-%m-%d' )
        end = datetime.datetime.strptime( str(time_end), '%Y-%m-%d' )
        period1 = start - initial
        period2 = end - initial
        s1 = period1.days * days
        s2 = period2.days * days
        url ="https://query1.finance.yahoo.com/v7/finance/download/"+stock_id+".TW?period1="+str(s1)+"&period2="+str(s2)+"&interval=1d&events=history&includeAdjustedClose=true" 
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36"}
        response = requests.get(url,headers = headers)
        #response.text
        df = pd.read_csv(StringIO(response.text),index_col = "Date",parse_dates = ["Date"])
    
        break
    except:
        print("輸入錯誤格式，請重新輸入")
df.Close.plot(figsize=(12,5))