from aiogram import Dispatcher, Router, types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from tiktok_bot.apps.bot import const
from tiktok_bot.apps.bot.filters.base_filters import UserFilter, ChannelSubscriptionFilter
from tiktok_bot.db.models import User

router = Router()


async def start(message: types.Message | types.CallbackQuery, user: User, state: FSMContext):
    if isinstance(message, types.CallbackQuery):
        message = message.message
    await state.clear()
    await message.answer(const.start_message,
                         # reply_markup=markups.common_menu.start_menu()
                         )


async def help_message(message: types.Message, user: User, state: FSMContext):
    await state.clear()
    await message.answer(const.start_message)


async def history(message: types.Message, user: User, state: FSMContext):
    await state.clear()
    await user.fetch_related("adv_user")
    await message.answer(f"Вы скачали: {user.adv_user.download_count} видео!")


async def not_link(message: types.Message):
    await message.answer("Я тебя не понял, отправь мне ссылку на видео TikTok.\n"
                         "Формат ссылки: https://vm.tiktok.com или https://www.tiktok.com",
                         reply_markup=ReplyKeyboardRemove())


def register_common(dp: Dispatcher):
    dp.include_router(router)

    callback = router.callback_query.register
    message = router.message.register

    message(start, UserFilter(), ChannelSubscriptionFilter(), commands="start", state="*")
    callback(start, UserFilter(), ChannelSubscriptionFilter(), text="start", state="*")
    message(help_message, UserFilter(), commands="help", state="*")
    message(history, UserFilter(), text_startswith="🔍", state="*")
    message(not_link, state="*")
