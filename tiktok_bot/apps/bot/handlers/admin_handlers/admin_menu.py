from aiogram import Dispatcher, F, Router, types
from aiogram.dispatcher.fsm.context import FSMContext
# from aiogram.dispatcher.filters
from aiogram.dispatcher.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove
from loguru import logger

from tiktok_bot.apps.bot import markups
from tiktok_bot.apps.bot.callback_data.base_callback import ChatCallback
from tiktok_bot.config.config import config
from tiktok_bot.db.models import User
from tiktok_bot.db.models.base import Chat
from tiktok_bot.loader import bot

router = Router()


class SendMail(StatesGroup):
    send = State()


class NewChat(StatesGroup):
    done = State()


async def admin_start(message: types.CallbackQuery | types.Message, state: FSMContext):
    await state.clear()
    if isinstance(message, types.CallbackQuery):
        message = message.message
    await message.answer(f"Выберите функцию", reply_markup=markups.admin_menu.admin_start())


async def view_chats(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    chats = await Chat.all()
    await call.message.answer(f"Все чаты:", reply_markup=markups.admin_menu.view_chats(chats))


async def new_chat(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.answer(f"Добавьте бота в чат и сделайте администратором, чтобы проверять подписки.\n"
                              f"Введите ссылку на канал", reply_markup=ReplyKeyboardRemove())
    await state.set_state(NewChat.done)


async def new_chat_done(message: types.Message, state: FSMContext):
    await state.clear()
    await Chat.create(link=message.text)
    await message.answer("Чат для подписки успешно добавлен")


async def touch_chat(call: types.CallbackQuery, callback_data: ChatCallback, state: FSMContext):
    await state.clear()
    chat = await Chat.get(pk=callback_data.pk)
    await call.message.answer(f"{chat.link}",
                              reply_markup=markups.admin_menu.touch_chat(chat))


async def delete_chat(call: types.CallbackQuery, callback_data: ChatCallback, state: FSMContext):
    await state.clear()
    await state.update_data(delete_chat=callback_data.pk)
    chat = await Chat.get(pk=callback_data.pk)
    await chat.delete()
    await call.message.answer("Чат успешно удален")


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
    callback(view_chats, ChatCallback.filter(F.action == "view"), state="*")
    callback(new_chat, ChatCallback.filter(F.action == "new"), state="*")
    message(new_chat_done, state=NewChat.done)

    callback(touch_chat, ChatCallback.filter(F.action == "touch"), state="*")
    callback(delete_chat, ChatCallback.filter(F.action == "delete"), state="*")
