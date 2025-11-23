import os
from aio_pika import connect_robust, Message, ExchangeType
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_URL = os.getenv("RABBITMQ_URL")
QUEUE_NAME = os.getenv("RABBITMQ_QUEUE")


class FastStream:
    def __init__(self):
        self.conn = None
        self.channel = None
        self.exchange = None

    async def connect(self):
        if self.conn:
            return
        self.conn = await connect_robust(RABBITMQ_URL)
        self.channel = await self.conn.channel()
        self.exchange = await self.channel.declare_exchange(
            "transflow_exchange", ExchangeType.FANOUT
        )
        await self.channel.declare_queue(QUEUE_NAME, durable=True)

    async def publish(self, routing_key: str, body: bytes):
        await self.connect()
        await self.exchange.publish(Message(body), routing_key="")


async def consume(callback):
    conn = await connect_robust(RABBITMQ_URL)
    channel = await conn.channel()
    queue = await channel.declare_queue(QUEUE_NAME, durable=True)

    async with queue.iterator() as queue_iter:
        async for msg in queue_iter:
            async with msg.process():
                await callback(msg.body)
