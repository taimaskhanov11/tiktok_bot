from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from tiktok_bot.apps.bot import temp
from tiktok_bot.config.config import config


class BotMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message | CallbackQuery, dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: dict[str, Any]
    ) -> Any:
        # print(f"{data=}")
        # print(f"{event=}")
        # print(f"{handler=}")
        # print(BOT_RUNNING)
        if temp.BOT_RUNNING or event.from_user.id in config.bot.admins:
            return await handler(event, data)
