from fastapi import FastAPI

from app.handlers.price import router as prices_router

app_fastapi = FastAPI()

app_fastapi.include_router(prices_router)
