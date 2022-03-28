from fastapi import APIRouter

from database import SESSION
from database import Stock, database_Stock, Favorite, database_Favorite

router = APIRouter()

@router.get("/home/stock")
async def get_stock(numbers: int):
    data = SESSION.query(database_Stock).filter(database_Stock.number == numbers).first()
    SESSION.close()
    return data

@router.get("/home/user")
async def get_favorite(user: str):
    user_favorite = SESSION.query(database_Favorite).filter(database_Favorite.user == user).all()
    SESSION.close()
    return user_favorite

@router.put("/home")
async def add_stock(stock_info: Stock):
    new_stack_info = database_Stock(
        **{
            "number": stock_info.number,
            "name": stock_info.name,
            "high_price": stock_info.high_price,
            "low_price": stock_info.low_price,
            "start_price": stock_info.start_price,
            "now_price": stock_info.now_price,
            "price_increase": stock_info.price_increase
        }
    )
    SESSION.add(new_stack_info)
    SESSION.commit()
    SESSION.refresh(new_stack_info)
    return stock_info