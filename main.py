from fastapi import FastAPI
from config import Config

from routers import home

from fakedata import add_fakedata

app = FastAPI()
app.include_router(home.router)

if Config.FAKE_DATA == "true":
    add_fakedata()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host=Config.HOST, port=Config.PORT) 