from aiogram import Dispatcher, F, Router, types
from aiogram.dispatcher.fsm.context import FSMContext
# from aiogram.dispatcher.filters
from aiogram.dispatcher.fsm.state import StatesGroup, State
from loguru import logger

from tiktok_bot.apps.bot import markups
from tiktok_bot.config.config import config
from tiktok_bot.db.models import User
from tiktok_bot.loader import bot

router = Router()


class SendMail(StatesGroup):
    send = State()


async def admin_start(message: types.CallbackQuery | types.Message, state: FSMContext):
    await state.clear()
    if isinstance(message, types.CallbackQuery):
        message = message.message
    await message.answer(f"Выберите функцию", reply_markup=markups.admin_menu.admin_start())

async def users_count(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    users_count_num = await User.all().count()
    await call.message.answer(f"В боте зарегистрировано: {users_count_num} 👥",
                              reply_markup=markups.admin_menu.admin_button())


async def send_mail(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.answer(f"Введите текст для рассылки всем пользователям",
                              reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(SendMail.send)


async def send_mail_done(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Идет отправка...")
    users = await User.all()
    for user in users:
        try:
            await bot.send_message(user.user_id, message.text, "markdown")
        except Exception as e:
            logger.warning(e)
    await message.answer(f"Рассылка отправлена {len(users)} пользователям")


def register_admin(dp: Dispatcher):
    dp.include_router(router)
    router.message.filter(F.from_user.id.in_(config.bot.admins))

    callback = router.callback_query.register
    message = router.message.register

    message(admin_start, commands="admin", state="*")
    callback(admin_start, text="admin", state="*")
    callback(send_mail, text="send_mail", state="*")
    message(send_mail_done, state=SendMail.send)
    callback(users_count, text="users_count", state="*")
