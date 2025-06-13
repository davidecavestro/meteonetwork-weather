"""Limit requests to REST api endpoints from MeteoNetwork Weather component."""
import asyncio
from datetime import datetime, timedelta

class RateLimiter:
    """API requests limiter."""

    def __init__(self, rate_limit=1):
        """Initialize the rate limiter."""
        self.rate_limit = rate_limit  # Requests per minute
        self._last_request_time = datetime.min
        self._lock = asyncio.Lock()

    async def throttle(self, request_callable):
        """Throttles execution of the given request callable based on rate limit.

        :param request_callable: A callable (e.g., lambda) that performs the request.
        :return: The result of the callable.
        """
        async with self._lock:
            now = datetime.now()
            wait_time = (self._last_request_time + timedelta(minutes=1 / self.rate_limit)) - now
            if wait_time.total_seconds() > 0:
                await asyncio.sleep(wait_time.total_seconds())

            self._last_request_time = datetime.now()
            return await request_callable()
