from fastapi import FastAPI
from config import Config

from routers import home

app = FastAPI()
app.include_router(home.router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host=Config.HOST, port=Config.PORT) 