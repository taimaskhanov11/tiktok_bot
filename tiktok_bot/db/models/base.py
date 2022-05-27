import datetime
from typing import Type, Optional, Any

from loguru import logger
from tortoise import fields, models, BaseDBAsyncClient
from tortoise.functions import Sum
from tortoise.models import MODEL

from tiktok_bot.apps.bot import temp

__all__ = (
    "User",
    "Chat",
    "SponsorChat",
    "AdvUser"
)


class Chat(models.Model):
    skin = fields.CharField(100, index=True)
    link = fields.CharField(100, index=True)

    def __str__(self):
        return f"{self.skin} [{self.link}]"

    @classmethod
    async def create(cls, **kwargs):
        print(temp.SUBSCRIPTION_CHANNELS)
        temp.SUBSCRIPTION_CHANNELS.append((kwargs.get("skin"), kwargs.get("link")))
        return await super().create(**kwargs)

    async def delete(self, using_db=None) -> None:
        print(temp.SUBSCRIPTION_CHANNELS)
        temp.SUBSCRIPTION_CHANNELS.remove(self.tuple)
        await super().delete(using_db)

    @property
    def tuple(self) -> tuple[str, str]:
        return self.skin, self.link

    def add_to_temp(self):
        temp.SUBSCRIPTION_CHANNELS.append(self.tuple)

    def remove_from_temp(self):
        temp.SUBSCRIPTION_CHANNELS.remove(self.tuple)


class SponsorChat(models.Model):
    skin = fields.CharField(100, index=True)
    link = fields.CharField(100, index=True)
    views = fields.IntField()
    done = fields.IntField(default=0)

    def __str__(self):
        return f"{self.skin} [{self.link}]"

    async def incr_view(self):
        self.done += 1
        # self.done = F('done') + 1
        # print(self.done)
        if self.done >= self.views:
            await self.delete()
        else:
            await self.save(update_fields=["done"])

    @property
    def tuple(self) -> tuple[str, str, str, str]:
        return self.skin, self.link, self.views, self.done

    def add_to_temp(self):
        temp.SPONSOR_CHANNELS.append(self.tuple)

    def remove_from_temp(self):
        temp.SPONSOR_CHANNELS.remove(self.tuple)


class User(models.Model):
    user_id = fields.BigIntField(index=True, unique=True)
    username = fields.CharField(32, unique=True, index=True, null=True)
    first_name = fields.CharField(255, null=True)
    last_name = fields.CharField(255, null=True)
    language = fields.CharField(32, default="ru")
    is_search = fields.BooleanField(default=False)
    # adv_user: fields.OneToOneNullableRelation["AdvUser"]
    adv_user: "AdvUser"

    @classmethod
    async def create(cls: Type[MODEL], using_db: Optional[BaseDBAsyncClient] = None, **kwargs: Any) -> MODEL:
        user = await super().create(using_db, **kwargs)
        await AdvUser.create(user=user)
        return user

    @classmethod
    async def count_all(cls):
        return await cls.all().count()

    @classmethod
    async def count_new_today(cls) -> int:
        return await cls.filter(adv_user__registered_at=datetime.date.today()).count()

    @classmethod
    async def reset_is_search(cls):
        count = await cls.filter(is_search=True).update(is_search=False)
        logger.trace(f"Сброс состояния поиска: {count}")

    async def __aenter__(self):
        # Включение режима блокировки пока запрос не завершиться
        self.is_search = True
        await self.save()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Отключение режима поиска
        self.is_search = False
        await self.save(update_fields=["is_search"])
        if exc_type:
            logger.exception(f"{exc_type}, {exc_val}, {exc_tb}")


# class Download(models.Model):
#     count = fields.IntField()
#     time = fields.DatetimeField()

class AdvUser(models.Model):
    user: fields.OneToOneRelation[User] = fields.OneToOneField("models.User", related_name="adv_user")
    registered_at = fields.DatetimeField(auto_now_add=True)
    download_count = fields.IntField(default=0)

    # todo 5/27/2022 10:18 AM taima:

    async def incr_download(self):
        self.download_count += 1
        await self.save(update_fields=["download_count"])

    @classmethod
    async def all_downloads(cls) -> int:
        return (await cls.all().annotate(count=Sum("download_count")).values("count"))[0].get("count")
