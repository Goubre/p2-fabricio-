from fastapi import FastAPI
from typing import List
import asyncio

from src.models.corrida_model import Corrida
from src.database.mongo_client import corridas_collection
from src.database.redis_client import get_redis
from src import producer

app = FastAPI(title="TransFlow API")


@app.post("/corridas")
async def create_corrida(corrida: Corrida):
    data = corrida.dict()

    await corridas_collection.update_one(
        {"id_corrida": data["id_corrida"]}, {"$set": data}, upsert=True
    )

    asyncio.create_task(producer.publish_corrida(data))
    return {"status": "ok", "id_corrida": data["id_corrida"]}


@app.get("/corridas", response_model=List[Corrida])
async def list_corridas():
    docs = await corridas_collection.find().to_list(1000)
    return docs


@app.get("/corridas/{forma}", response_model=List[Corrida])
async def filter_corridas(forma: str):
    docs = await corridas_collection.find({"forma_pagamento": forma}).to_list(1000)
    return docs


@app.get("/saldo/{motorista}")
async def get_saldo(motorista: str):
    redis = await get_redis()
    key = f"saldo:{motorista.lower()}"
    val = await redis.get(key)
    return {"motorista": motorista, "saldo": float(val or 0)}
