from aiogram import Dispatcher, Router, types
from aiogram.dispatcher.fsm.context import FSMContext

from tiktok_bot.apps.bot import const
from tiktok_bot.apps.bot.filters.base_filters import UserFilter
from tiktok_bot.apps.bot.handlers.utils import channel_status_check
from tiktok_bot.config.config import config
from tiktok_bot.db.models import User

router = Router()


async def start(message: types.Message, user: User, state: FSMContext):
    await state.clear()

    if not await channel_status_check(message.from_user.id):
        channels = "\n".join(config.bot.chats)
        await message.answer(f"Для того, чтобы пользоваться ботом, нужно подписаться на каналы:\n{channels}")
        return
    await message.answer(const.start_message,
                         # reply_markup=markups.common_menu.start_menu()
                         )


async def help_message(message: types.Message, user: User, state: FSMContext):
    await state.clear()
    await message.answer(const.start_message)


async def not_link(message: types.Message):
    await message.answer("Я тебя не понял, отправь мне ссылку на видео TikTok.\n"
                         "Формат ссылки: https://vm.tiktok.com или https://www.tiktok.com")


def register_common(dp: Dispatcher):
    dp.include_router(router)

    callback = router.callback_query.register
    message = router.message.register

    message(start, UserFilter(), commands="start", state="*")
    message(help_message, UserFilter(), commands="help", state="*")
    message(not_link, state="*")
