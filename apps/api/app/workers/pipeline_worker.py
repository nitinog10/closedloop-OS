from __future__ import annotations

import asyncio

import orjson
from aiokafka import AIOKafkaConsumer

from app.core.config import settings


class PipelineWorker:
    def __init__(self) -> None:
        self.consumer = AIOKafkaConsumer(
            'canonical-events.normalized',
            'canonical-events.embedded',
            'knowledge-graph.upserted',
            bootstrap_servers=settings.kafka_bootstrap_servers,
            group_id='closedloop-pipeline-workers',
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
                        await self.handle_message(message.topic, message.value)
        finally:
            await self.consumer.stop()

    async def handle_message(self, topic: str, payload: dict) -> None:
        # Replace with durable handlers for enrichment, graph persistence,
        # observability, and downstream action scheduling.
        await asyncio.sleep(0)
        _ = (topic, payload)


if __name__ == '__main__':
    asyncio.run(PipelineWorker().run())
