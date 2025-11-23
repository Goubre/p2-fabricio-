import json
from src.faststream import FastStream

stream = FastStream()


async def publish_corrida(corrida: dict):
    body = json.dumps({"event": "corrida_finalizada", "data": corrida}).encode()
    await stream.publish("corrida_finalizada", body)
