import time
from collections import defaultdict, deque

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class InMemoryRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute: int = 120):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.buckets: dict[str, deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else 'unknown'
        now = time.time()
        bucket = self.buckets[client_ip]

        while bucket and now - bucket[0] > 60:
            bucket.popleft()

        if len(bucket) >= self.requests_per_minute:
            return JSONResponse(status_code=429, content={'detail': 'Rate limit exceeded'})

        bucket.append(now)
        return await call_next(request)
