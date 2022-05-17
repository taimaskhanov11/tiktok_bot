import asyncio
import logging

from aiogram import Bot
from aiogram.types import BotCommand

from tiktok_bot.apps.bot.handlers.admin_handlers.admin_menu import register_admin
from tiktok_bot.apps.bot.handlers.common_menu import register_common
from tiktok_bot.apps.bot.handlers.downloader_menu import register_downloader
from tiktok_bot.apps.bot.handlers.errors_handlers import register_error
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

    # Регистрация хэндлеров
    register_admin(dp)
    register_downloader(dp)
    register_common(dp)
    register_error(dp)
    # Регистрация middleware

    # Регистрация фильтров

    await dp.start_polling(bot, skip_updates=True)


def main():
    asyncio.run(start())
    asyncio.get_event_loop()


if __name__ == "__main__":
    main()
