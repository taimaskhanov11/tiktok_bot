from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext
# from aiogram.dispatcher.filters
from aiogram.dispatcher.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove

from tiktok_bot.apps.bot import markups, temp
from tiktok_bot.apps.bot.handlers.utils import MailSender, MailStatus

router = Router()


class SendMail(StatesGroup):
    preview = State()
    select = State()

    button = State()
    send = State()


async def send_mail(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.answer(f"Введите текст для рассылки всем пользователям",
                              reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(SendMail.preview)


async def send_mail_preview(message: types.Message, state: FSMContext):
    await state.update_data(mail=message.text)
    await message.answer(message.text, reply_markup=markups.admin_menu.send_mail_preview())
    await state.set_state(SendMail.select)


async def send_mail_add_button_start(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Отправьте мне список URL-кнопок в одном сообщении. Следуйте этому формату:\n"
                              "Кнопка 1 - https://www.example1.com\n"
                              "Кнопка 2 - https://www.example2.com\n\n"
                              "Используйте разделитель |, чтобы добавить до трех кнопок в один ряд. Например:\n"
                              "Кнопка 1 - https://www.example1.com |\n"
                              "Кнопка 2 - https://www.example2.com\n"
                              "Кнопка 3 - https://www.example3.com |\n"
                              "Кнопка 4 - https://www.example4.com\n",
                              reply_markup=ReplyKeyboardRemove())
    await state.set_state(SendMail.button)


async def send_mail_add_button(message: types.Message, state: FSMContext):
    data = await state.get_data()
    markup = markups.admin_menu.send_mail_add_button(message.text)
    await message.answer(data["mail"], reply_markup=markup)
    await state.update_data(markup=markup)
    await state.set_state(SendMail.select)


async def send_mail_done(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Идет отправка...")
    data = await state.get_data()
    await state.clear()
    sender = MailSender(message=call.message, mail=data.get("mail"), markup=data.get("markup"))
    if temp.MAIL_SENDER:
        temp.MAIL_SENDER.status = MailStatus.stop
    temp.MAIL_SENDER = sender
    await sender.send_mail()


async def send_mail_pause(call: types.CallbackQuery):
    temp.MAIL_SENDER.status = MailStatus.pause
    await temp.MAIL_SENDER.status_message.edit_reply_markup(
        markups.admin_menu.send_mail_done(False)
    )


async def send_mail_continue(call: types.CallbackQuery):
    temp.MAIL_SENDER.status = MailStatus.run
    await temp.MAIL_SENDER.status_message.edit_reply_markup(
        markups.admin_menu.send_mail_done()
    )


async def send_mail_stop(call: types.CallbackQuery):
    temp.MAIL_SENDER.status = MailStatus.stop


def register_send_mail(dp: Router):
    dp.include_router(router)

    callback = router.callback_query.register
    message = router.message.register

    callback(send_mail, text="send_mail", state="*")
    message(send_mail_preview, state=SendMail.preview)

    callback(send_mail_add_button_start, text="add_button", state=SendMail.select)
    message(send_mail_add_button, state=SendMail.button)

    callback(send_mail_done, text="accept", state=SendMail.select)
    callback(send_mail_pause, text="pause_mail", state="*")
    callback(send_mail_continue, text="continue_mail", state="*")
    callback(send_mail_stop, text="stop_mail", state="*")
