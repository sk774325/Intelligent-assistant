import json

from database import SESSION
from database import database_Stock, database_Favorite


def add_fakedata():
    #stock fakedata
    fakedata_stock = json.load(open("fakedata_stock.json"))
    for data in enumerate(fakedata_stock):
        new_stock = database_Stock(
            **{
                "number": fakedata_stock["number"],
                "name": fakedata_stock["name"],
                "high_price": fakedata_stock["high_price"],
                "low_price": fakedata_stock["low_price"],
                "start_price": fakedata_stock["start_price"],
                "now_price": fakedata_stock["now_price"],
                "price_increase": fakedata_stock["price_increase"]
            }
        )
    SESSION.add(new_stock)
    SESSION.commit()
    SESSION.refresh(new_stock)