import asyncio
import random

from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import StatesGroup, State

from tiktok_bot.apps.bot import temp
from tiktok_bot.apps.bot.markups.admin import bot_settings_markups

router = Router()


class SendMail(StatesGroup):
    preview = State()
    select = State()

    button = State()
    send = State()


async def bot_setting_start(call: types.CallbackQuery, state: FSMContext, **kwargs):
    await state.clear()
    status = "✅ Запущен" if temp.BOT_RUNNING else "🚫 Приостановлен"
    await call.message.answer("Панель управления ботом\n"
                              f"Статус бота:\n{status}", reply_markup=bot_settings_markups.bot_setting_start())


async def start_bot_view(call):
    send_text = "🤖 Производиться запуск бота ожидайте...\n1"
    message = await call.message.answer(send_text)
    for text in ["Проверка целостности",
                 "Проверка конфигурации",
                 "Проверка базы данных",
                 "Проверка протоколов",
                 "Оптимизация"]:
        for sign in ["⏳", "⌛", "✅"]:
            await asyncio.sleep(random.uniform(0, 1))
            add_text = f"\n▶ {text} {sign}"
            await message.edit_text(f"{send_text}{add_text}")
        send_text += add_text


async def run_bot(call: types.CallbackQuery):
    temp.BOT_RUNNING = True
    await start_bot_view(call)
    await call.message.edit_reply_markup(bot_settings_markups.bot_setting_start())
    await call.message.answer("✅ Бот успешно запущен")


async def stop_bot(call: types.CallbackQuery):
    temp.BOT_RUNNING = False
    await call.message.edit_reply_markup(bot_settings_markups.bot_setting_start())
    edit_message = await call.message.answer("🕐 Приостановка бота")
    await asyncio.sleep(random.uniform(0, 1))
    await edit_message.edit_text("✅ Бот приостановлен")


async def restart_bot(call: types.CallbackQuery):
    await call.message.answer("Перезапуск бота ожидайте...")
    temp.BOT_RUNNING = False
    await start_bot_view(call)
    temp.BOT_RUNNING = True
    await call.message.answer("Бот перезапущен")


def register_bot_settings(dp: Router):
    dp.include_router(router)

    callback = router.callback_query.register
    message = router.message.register

    callback(bot_setting_start, text="bot_settings", state="*")

    callback(run_bot, text="run_bot", state="*")
    callback(stop_bot, text="stop_bot", state="*")
    callback(restart_bot, text="restart_bot", state="*")
