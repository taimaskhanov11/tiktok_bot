from aiogram import types
from aiogram.dispatcher.filters import BaseFilter
from loguru import logger

from tiktok_bot.apps.bot.handlers.utils import channel_status_check
from tiktok_bot.config.config import config
from tiktok_bot.db.models import User


class UserFilter(BaseFilter):
    async def __call__(self, update: types.CallbackQuery | types.Message) -> dict[str, User]:
        user = update.from_user
        user, is_new = await User.get_or_create(
            user_id=user.id,
            defaults={
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "language": user.language_code,
            },
        )
        if is_new:
            logger.info(f"Новый пользователь {user=}")
        return {"user": user}


class ChannelSubscriptionFilter(BaseFilter):
    async def __call__(self, message: types.Message):
        if await channel_status_check(message.from_user.id):
            return True
        channels = "\n".join(config.bot.chats)
        await message.answer(f"Для того, чтобы пользоваться ботом, нужно подписаться на каналы:\n{channels}")
        return False
