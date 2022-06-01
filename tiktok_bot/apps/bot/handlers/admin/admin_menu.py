from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext
# from aiogram.dispatcher.filters
from aiogram.dispatcher.fsm.state import StatesGroup, State
from aiogram.utils.chat_action import ChatActionSender

from tiktok_bot.apps.bot.handlers.utils import parse_user_fields, part_sending
from tiktok_bot.apps.bot.markups.admin import admin_markups
from tiktok_bot.db.models import User

router = Router()


class NewChat(StatesGroup):
    done = State()


class ExportUsers(StatesGroup):
    choice_send_type = State()
    finish = State()


async def admin_start(message: types.CallbackQuery | types.Message, state: FSMContext):
    await state.clear()
    if isinstance(message, types.CallbackQuery):
        message = message.message
    await message.answer(f"Выберите функцию", reply_markup=admin_markups.admin_start())


async def export_users(call: types.CallbackQuery | types.Message, state: FSMContext):
    await state.clear()
    await call.message.answer(f"Какие поля нужны для экспорта:\n"
                              f"1.user_id\n"
                              f"2.username\n"
                              f"3.first_name\n"
                              f"4.last_name\n"
                              f"0.Все поля\n"
                              f"Отправьте комбинацию нужных полей", reply_markup=admin_markups.back())
    await state.set_state(ExportUsers.choice_send_type)


async def export_users_send_type(message: types.Message, state: FSMContext):
    await state.update_data(fields=message.text)
    await message.answer(f"В каком виде экспортировать пользователей",
                         reply_markup=admin_markups.export_users_send_type())
    await state.set_state(ExportUsers.finish)


async def export_users_finish(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    fields = parse_user_fields(data["fields"])
    result = await User.export_users(_fields=fields, _to=call.data)
    if call.data == "text":
        async with ChatActionSender.typing(bot=call.message.via_bot, chat_id=call.from_user.id):
            await part_sending(call.message, result)
    else:
        async with ChatActionSender.upload_document(bot=call.message.via_bot, chat_id=call.from_user.id):
            await call.message.answer_document(result)
    await call.message.answer("Пользователи выгружены", reply_markup=admin_markups.back())

    # await state.clear()


def register_admin(dp: Router):
    dp.include_router(router)

    callback = router.callback_query.register
    message = router.message.register

    message(admin_start, commands="admin", state="*")
    callback(admin_start, text="admin", state="*")
    callback(export_users, text="export_users", state="*")
    message(export_users_send_type, state=ExportUsers.choice_send_type)
    callback(export_users_finish, state=ExportUsers.finish)
