# run using: $ uvicorn main:app --host 127.0.0.1 --port 8000 --reload

from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.postgres import init_postgres, close_postgres
from routes.product_routes import sensor_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_postgres()
    yield
    await close_postgres()


app: FastAPI = FastAPI(lifespan=lifespan, title="FastAPI TimescaleDB Sensor Data API")
app.include_router(sensor_router)