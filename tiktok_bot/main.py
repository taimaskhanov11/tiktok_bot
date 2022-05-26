import asyncio
import logging

from aiogram import Bot
from aiogram.types import BotCommand

from tiktok_bot.apps.bot.handlers.admin import register_admin_handlers
from tiktok_bot.apps.bot.handlers.common.common_menu import register_common
from tiktok_bot.apps.bot.handlers.common.downloader_menu import register_downloader
from tiktok_bot.apps.bot.handlers.errors_handlers import register_error
from tiktok_bot.apps.bot.utils.init import init_chats
from tiktok_bot.config.config import config
from tiktok_bot.config.logg_settings import init_logging
from tiktok_bot.db import init_db
from tiktok_bot.loader import bot, dp


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Главное меню"),
        BotCommand(command="/admin", description="Админ меню"),
        BotCommand(command="/help", description="Помощь"),
    ]
    await bot.set_my_commands(commands)


async def start():
    # Настройка логирования
    init_logging(
        old_logger=True,
        level="TRACE",
        # old_level=logging.DEBUG,
        old_level=logging.INFO,
        steaming=True,
        write=True,
    )

    # dp.startup.register(on_startup)
    # dp.shutdown.register(on_shutdown)

    # Установка команд бота
    await set_commands(bot)

    # Инициализация бд
    await init_db(**config.db.dict())

    # Меню админа
    # dp.message.filter(F.chat.type == "private")
    # Регистрация хэндлеров
    # register_admin(dp)
    register_admin_handlers(dp)
    register_downloader(dp)
    register_common(dp)
    register_error(dp)
    # Регистрация middleware
    # dp.message.middleware(CounterMiddleware())
    # todo 5/26/2022 8:47 PM taima: добавить миддлваре
    # dp.message.outer_middleware(CounterMiddleware())
    # Регистрация фильтров

    await init_chats()
    await dp.start_polling(bot, skip_updates=True)


def main():
    asyncio.run(start())
    asyncio.get_event_loop()


if __name__ == "__main__":
    main()
