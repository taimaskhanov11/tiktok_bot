from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext
# from aiogram.dispatcher.filters
from aiogram.dispatcher.fsm.state import StatesGroup, State

from tiktok_bot.apps.bot.markups.admin import admin_markups

router = Router()


class NewChat(StatesGroup):
    done = State()


async def admin_start(message: types.CallbackQuery | types.Message, state: FSMContext):
    await state.clear()
    if isinstance(message, types.CallbackQuery):
        message = message.message
    await message.answer(f"Выберите функцию", reply_markup=admin_markups.admin_start())


def register_admin(dp: Router):
    dp.include_router(router)

    callback = router.callback_query.register
    message = router.message.register

    message(admin_start, commands="admin", state="*")
    callback(admin_start, text="admin", state="*")
