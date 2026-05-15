from __future__ import annotations

import asyncio

from aiokafka import AIOKafkaConsumer
import orjson

from app.core.config import settings


class GraphWorker:
    def __init__(self) -> None:
        self.consumer = AIOKafkaConsumer(
            'canonical-events.embedded',
            bootstrap_servers=settings.kafka_bootstrap_servers,
            group_id='closedloop-graph-workers',
            enable_auto_commit=True,
            value_deserializer=lambda value: orjson.loads(value),
        )

    async def run(self) -> None:
        await self.consumer.start()
        try:
            while True:
                batch = await self.consumer.getmany(timeout_ms=1000, max_records=100)
                for _, messages in batch.items():
                    for message in messages:
                        await self.handle_message(message.value)
        finally:
            await self.consumer.stop()

    async def handle_message(self, payload: dict) -> None:
        await asyncio.sleep(0)
        _ = payload


if __name__ == '__main__':
    asyncio.run(GraphWorker().run())
