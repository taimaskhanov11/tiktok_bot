from aiogram import F, Router, types
from aiogram.dispatcher.fsm.context import FSMContext
# from aiogram.dispatcher.filters
from aiogram.dispatcher.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove
from loguru import logger

from tiktok_bot.apps.bot.callback_data.base_callback import ChatCallback, SponsorChatCallback
from tiktok_bot.apps.bot.handlers.utils import parse_channel_link
from tiktok_bot.apps.bot.markups.admin import subscriptions_markups
from tiktok_bot.db.models.base import Chat, SponsorChat

router = Router()


class NewChat(StatesGroup):
    done = State()


class NewSponsorChat(StatesGroup):
    done = State()


async def view_chats(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    chats = await Chat.all()
    await call.message.answer(f"Все чаты для обязательной подписки:",
                              reply_markup=subscriptions_markups.view_chats(chats))


async def new_chat(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.answer(f"Добавьте бота в чат и сделайте администратором, чтобы проверять подписки.\n"
                              f"Введите ссылку на канал. "
                              f"Введите ссылку по которому должны будут пройти пользователи и через пробел фактическую ссылку на канал для проверки ботом\n"
                              f"Например:\n"
                              f"https://t.me/+bIBc0e-525k2MThi https://t.me/mychannel",
                              reply_markup=ReplyKeyboardRemove())
    await state.set_state(NewChat.done)


async def new_chat_done(message: types.Message, state: FSMContext):
    try:
        await state.clear()
        skin, link = parse_channel_link(message.text)
        chat = await Chat.create(skin=skin, link=link)
        await message.answer(f"Чат для подписки: {chat} успешно добавлен")
    except Exception as e:
        logger.warning(e)
        await message.answer("Неправильный ввод")


async def touch_chat(call: types.CallbackQuery, callback_data: ChatCallback, state: FSMContext):
    await state.clear()
    chat = await Chat.get(pk=callback_data.pk)
    await call.message.answer(f"{chat}",
                              reply_markup=subscriptions_markups.touch_chat(chat))


async def delete_chat(call: types.CallbackQuery, callback_data: ChatCallback, state: FSMContext):
    await state.clear()
    await state.update_data(delete_chat=callback_data.pk)
    chat = await Chat.get(pk=callback_data.pk)
    await chat.delete()
    await call.message.answer(f"Канал для подписки: {chat} успешно удален")


async def sponsor_view_chats(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    chats = await SponsorChat.all().order_by("id")
    answer = ""
    for num, chat in enumerate(chats):
        answer += f"{num}.{chat}. Выполнено {chat.done} из {chat.views}\n"
    await call.message.answer(f"Все спонсорские чаты:\n{answer}",
                              reply_markup=subscriptions_markups.sponsor_view_chats(chats),
                              disable_web_page_preview=True)


async def sponsor_new_chat(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.answer(f"Введите название кнопки, ссылку и количество необходимых просмотров через пробел\n"
                              f"Например:\n"
                              f"Подписывайтесь https://t.me/mychannel 500",
                              reply_markup=ReplyKeyboardRemove())
    await state.set_state(NewSponsorChat.done)


async def sponsor_new_chat_done(message: types.Message, state: FSMContext):
    try:
        await state.clear()
        skin, link, views = message.text.split()
        await SponsorChat.create(skin=skin, link=link, views=views)
        await message.answer("Спонсорский чат успешно добавлен")
    except Exception as e:
        logger.warning(e)
        await message.answer("Неправильный ввод")


async def sponsor_touch_chat(call: types.CallbackQuery, callback_data: SponsorChatCallback, state: FSMContext):
    await state.clear()
    chat = await SponsorChat.get(pk=callback_data.pk)
    await call.message.answer(f"{chat.link}",
                              reply_markup=subscriptions_markups.touch_chat(chat))


async def sponsor_delete_chat(call: types.CallbackQuery, callback_data: SponsorChatCallback, state: FSMContext):
    await state.clear()
    await state.update_data(delete_chat=callback_data.pk)
    chat = await SponsorChat.get(pk=callback_data.pk)
    await chat.delete()
    await call.message.answer(f"Спонсорский канал: {chat} успешно удален")


def register_subscriptions(dp: Router):
    dp.include_router(router)

    callback = router.callback_query.register
    message = router.message.register

    callback(view_chats, ChatCallback.filter(F.action == "view"), state="*")
    callback(new_chat, ChatCallback.filter(F.action == "new"), state="*")
    message(new_chat_done, state=NewChat.done)
    callback(touch_chat, ChatCallback.filter(F.action == "touch"), state="*")
    callback(delete_chat, ChatCallback.filter(F.action == "delete"), state="*")

    callback(sponsor_view_chats, SponsorChatCallback.filter(F.action == "view"), state="*")
    callback(sponsor_new_chat, SponsorChatCallback.filter(F.action == "new"), state="*")
    message(sponsor_new_chat_done, state=NewSponsorChat.done)
    callback(sponsor_touch_chat, SponsorChatCallback.filter(F.action == "touch"), state="*")
    callback(sponsor_delete_chat, SponsorChatCallback.filter(F.action == "delete"), state="*")
