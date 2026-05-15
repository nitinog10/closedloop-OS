import asyncio
from collections.abc import AsyncGenerator


async def stream_text(text: str) -> AsyncGenerator[bytes, None]:
    for chunk in text.split():
        yield f"data: {chunk} \n\n".encode("utf-8")
        await asyncio.sleep(0.02)
    yield b"data: [DONE]\n\n"
