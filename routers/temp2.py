def basic_draw(stock_id):
#資料轉換成DataFrame
#index_col : 將最左邊的行名稱以Date取代，不然沒寫這段行名稱會是從0開始的數字，而用Date取代是為了後續要畫圖、統計等處理上較方便
#parse_dates : 將csv中的時間字串轉換成日期格式，也是為了後續使用而改，不然字串無法被程式辨識成時間
#df = pd.read_csv(StringIO(response.text),index_col = "Date",parse_dates = ["Date"])
#df
#address = r"C:\users\y2k20\Desktop\\" + stock_id + ".csv" #自己改路徑
#df.to_csv(address)
###抓取 基本面跟籌碼面
    url_basic = "https://goodinfo.tw/tw/StockBzPerformance.asp?STOCK_ID="+stock_id
    headers_basic = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36"}
    res_basic = requests.get(url_basic,headers = headers_basic)
    res_basic.encoding = "utf-8"
    #res_basic.text
    soup = BeautifulSoup(res_basic.text,"lxml")
    data_basic = soup.select_one("#txtFinDetailData")

    dfs = pd.read_html(data_basic.prettify())
    df_basic = dfs[0]
    df_basic.columns = df_basic.columns.get_level_values(1)

    print(df_basic.head())