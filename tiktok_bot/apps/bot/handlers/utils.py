import re

from loguru import logger

from tiktok_bot.config.config import config
from tiktok_bot.loader import bot


async def channel_status_check(user_id):
    if config.bot.chats:
        results = []
        for chat in config.bot.chats:
            if '@' in chat:
                pass
            else:
                try:
                    chat = '@' + re.findall(r"t\.me/(.+)", chat)[0]
                except Exception as e:
                    logger.warning(e)
                    chat = '@' + chat

            try:
                member = await bot.get_chat_member(
                    chat_id=chat,
                    user_id=user_id,
                )
                # logger.trace(status)
                if member.status != "left":
                    results.append(True)
                else:
                    results.append(False)
            except Exception as e:
                logger.critical(e)
                results.append(True)
        return all(results)
    else:
        return True
