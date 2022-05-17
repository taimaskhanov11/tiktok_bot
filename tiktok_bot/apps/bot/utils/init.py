from loguru import logger

from tiktok_bot.config.config import config
from tiktok_bot.db.models import Chat


async def init_chats():
    logger.info("Initial chats")
    # print(await Chat.all())
    config.bot.chats = [chat.link for chat in await Chat.all()]
