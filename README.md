# Intelligent-assistant

## Function
- Predict the trends of Taiwan stock and cryptocurrency
- Each user can have his/her own favorite items

## Framework
- API : FastAPI
- Database - SQLite (Python)
- Server : uvicorn
- Language : Python, JavaScript

## API Format
### 1.Get stock info
+ /stock?numbers=2330
+ method:GET
+ body:none
+ response
```
{
    "low_price": 580,
    "name": "台積電",
    "now_price": 585,
    "start_price": 590,
    "number": 2330,
    "high_price": 600,
    "price_increase": -5
}
```

### 2.Get user favorite
+ /favorite?user=Jay
+ method:GET
+ body:none
+ response:
```
[
  {
    "number": 0,
    "name": "大盤指數",
    "high_price": 17500,
    "low_price": 17304,
    "start_price": 17444,
    "now_price": 17374,
    "price_increase": -70
  },
  {
    "low_price": 580,
    "name": "台積電",
    "now_price": 585,
    "start_price": 590,
    "number": 2330,
    "high_price": 600,
    "price_increase": -5
  },
  {
    "low_price": 960,
    "name": "聯發科",
    "now_price": 980,
    "start_price": 970,
    "number": 2454,
    "high_price": 1000,
    "price_increase": 10
  },
  {
    "low_price": 134,
    "name": "元大台灣50",
    "now_price": 134.7,
    "start_price": 134.5,
    "number": 50,
    "high_price": 136,
    "price_increase": 0.2
  },
  {
    "low_price": 105,
    "name": "鴻海",
    "now_price": 106.5,
    "start_price": 106,
    "number": 2317,
    "high_price": 107,
    "price_increase": 0.5
  }
]
```

### 3.Sign up new user
- /sign_up/Shon?user_pwd=12344&comfirm_pwd=12344
- Method:GET
- Response
```
{
    'Successful':False,
    'Comfirm_pwd_wrongly':False,
    'Used_ID':False
}
```


### 4.Log in 
- /log_in/Shon?user_pwd=12344
- Method:GET
- Response
```
{
    'Registered':False,
    'Successful':False,
}
```
