import logging

from aiogram import Dispatcher, Router
from loguru import logger

router = Router()

logger = logging.getLogger()


async def error_handler(update, exception):
    logger.exception(f"{exception}|{update}")
    return True


def register_error(dp: Dispatcher):
    dp.include_router(router)
    router.errors.register(error_handler)
