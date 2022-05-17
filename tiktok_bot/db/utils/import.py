import asyncio
import collections

from loguru import logger

from tiktok_bot.config.config import BASE_DIR, config
from tiktok_bot.db import init_db
from tiktok_bot.db.models import User

backup_name = f"db_backup"
BACKUP_DIR = BASE_DIR / "backup"
BACKUP_DIR.mkdir(exist_ok=True)


async def import_users():
    logger.debug("Выгрузка юзеров")
    users = ""

    for u in await User.all():
        users += f"{u.user_id}\n"
    with open(BASE_DIR / "users.txt", "w", encoding="utf-8") as f:
        f.write(users)
    logger.info(f"Выгрузка завершена")


async def main():
    await init_db(**config.db.dict())
    await import_users()


if __name__ == "__main__":
    asyncio.run(main())
