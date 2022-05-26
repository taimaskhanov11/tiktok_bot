from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message


class CounterMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0

    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: dict[str, Any]
    ) -> Any:
        self.counter += 1
        data['counter'] = self.counter
        print(data["counter"])
        print(data)
        print(event)
        # return await event.answer("asdas")
        return await handler(event, data)
