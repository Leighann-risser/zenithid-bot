from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable
from aiogram.types import TelegramObject

class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Inject user context or rate limiting logic here
        return await handler(event, data)