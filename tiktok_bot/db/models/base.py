from loguru import logger
from tortoise import fields, models

__all__ = (
    "User",
)


class User(models.Model):
    user_id = fields.BigIntField(index=True, unique=True)
    username = fields.CharField(32, unique=True, index=True, null=True)
    first_name = fields.CharField(255, null=True)
    last_name = fields.CharField(255, null=True)
    language = fields.CharField(32, default="ru")
    is_search = fields.BooleanField(default=False)

    async def __aenter__(self):
        # Включение режима блокировки пока запрос не завершиться
        self.is_search = True
        await self.save()
        return self

    # async def __aexit__(self, exc_type, exc_val, exc_tb):
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Отключение режима поиска
        self.is_search = False
        await self.save()
        if exc_type:
            logger.exception(f"{exc_type}, {exc_val}, {exc_tb}")
