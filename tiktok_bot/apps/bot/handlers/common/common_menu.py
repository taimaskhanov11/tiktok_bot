from aiogram import Dispatcher, Router, types
from aiogram.dispatcher.fsm.context import FSMContext

from tiktok_bot.apps.bot import const
from tiktok_bot.apps.bot.filters.base_filters import UserFilter, ChannelSubscriptionFilter
from tiktok_bot.db.models import User

router = Router()


async def start(message: types.Message, user: User, state: FSMContext):
    await state.clear()

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

    message(start, UserFilter(), ChannelSubscriptionFilter(), commands="start", state="*")
    message(help_message, UserFilter(), commands="help", state="*")
    message(not_link, state="*")
