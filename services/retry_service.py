import asyncio
from typing import Callable, Any
import logging

logger = logging.getLogger(__name__)

class RetryService:
    def __init__(
        self,
        max_retries: int = 3,
        delay: float = 1.0,
        backoff: float = 2.0
    ):
        self.max_retries = max_retries
        self.delay = delay
        self.backoff = backoff
    
    async def retry_async(
        self,
        func: Callable,
        *args,
        **kwargs
    ) -> Any:
        """异步重试机制"""
        last_exception = None
        current_delay = self.delay
        
        for attempt in range(self.max_retries):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                logger.warning(
                    f"Attempt {attempt + 1} failed: {str(e)}, "
                    f"retrying in {current_delay} seconds..."
                )
                await asyncio.sleep(current_delay)
                current_delay *= self.backoff
        
        logger.error(
            f"All {self.max_retries} attempts failed. "
            f"Last error: {str(last_exception)}"
        )
        raise last_exception
