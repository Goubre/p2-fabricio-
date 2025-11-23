import json
from src.faststream import consume
from src.database.redis_client import get_redis
from src.database.mongo_client import corridas_collection


async def process_message(body: bytes):
    payload = json.loads(body)
    data = payload.get("data")
    if not data:
        return

    motorista = data["motorista"]["nome"].lower()
    valor = float(data["valor_corrida"])

    redis = await get_redis()
    key = f"saldo:{motorista}"

    # ---- Atualização ATÔMICA do saldo usando pipeline (redis.asyncio) ----
    async with redis.pipeline(transaction=True) as pipe:
        while True:
            try:
                await pipe.watch(key)
                atual = await pipe.get(key)
                atual = float(atual) if atual else 0.0

                novo = atual + valor

                pipe.multi()
                pipe.set(key, novo)
                await pipe.execute()
                break

            except Exception:
                continue
            finally:
                await pipe.reset()

    # ---- Salvar ou atualizar a corrida no MongoDB ----
    await corridas_collection.update_one(
        {"id_corrida": data["id_corrida"]}, {"$set": data}, upsert=True
    )


async def start_consumer():
    await consume(process_message)
