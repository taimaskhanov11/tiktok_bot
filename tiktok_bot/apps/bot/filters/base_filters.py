from aiogram import types
from aiogram.dispatcher.filters import BaseFilter
from loguru import logger

from tiktok_bot.apps.bot.handlers.utils import channel_status_check
from tiktok_bot.apps.bot.markups.common import common_markups
from tiktok_bot.apps.bot.temp import ONLINE_USERS, SUBSCRIPTION_CHANNELS
from tiktok_bot.apps.bot.utils.base import run_user_online_status_deleter
from tiktok_bot.db.models import User


class UserFilter(BaseFilter):
    async def __call__(self, update: types.CallbackQuery | types.Message) -> dict[str, User]:
        user = update.from_user
        logger.trace(f"Update from @{user.username}[{user.id}]")
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

        # update online status
        if user.user_id not in ONLINE_USERS:
            ONLINE_USERS[user.user_id] = True
            run_user_online_status_deleter(user.user_id)

        return {"user": user}


class ChannelSubscriptionFilter(BaseFilter):
    async def __call__(self, message: types.Message | types.CallbackQuery):
        if isinstance(message, types.CallbackQuery):
            message = message.message
        if await channel_status_check(message.from_user.id):
            return True
        await message.answer(f"Для того, чтобы пользоваться ботом, нужно подписаться на каналы:\n",
                             reply_markup=common_markups.channel_status_check(SUBSCRIPTION_CHANNELS))
        return False
