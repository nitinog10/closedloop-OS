from __future__ import annotations

from abc import ABC, abstractmethod


class EventBus(ABC):
    @abstractmethod
    async def publish(self, topic: str, payload: dict) -> None:
        raise NotImplementedError


class InMemoryEventBus(EventBus):
    def __init__(self) -> None:
        self.messages: list[tuple[str, dict]] = []

    async def publish(self, topic: str, payload: dict) -> None:
        self.messages.append((topic, payload))


class KafkaEventBus(EventBus):
    def __init__(self, bootstrap_servers: str) -> None:
        self.bootstrap_servers = bootstrap_servers
        self._producer = None

    async def start(self) -> None:
        from aiokafka import AIOKafkaProducer

        if self._producer is None:
            self._producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)
            await self._producer.start()

    async def stop(self) -> None:
        if self._producer is not None:
            await self._producer.stop()
            self._producer = None

    async def publish(self, topic: str, payload: dict) -> None:
        import orjson

        if self._producer is None:
            await self.start()
        await self._producer.send_and_wait(topic, orjson.dumps(payload))
