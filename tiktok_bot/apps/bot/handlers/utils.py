import asyncio
import contextlib
import re
from enum import Enum
from unittest import mock

from aiogram import exceptions
from aiogram import types
from loguru import logger
from pydantic import BaseModel

from tiktok_bot.apps.bot import markups
from tiktok_bot.config.config import config
from tiktok_bot.db.models import User
from tiktok_bot.loader import bot


async def get_mock_users() -> list:
    user = await User.exclude(user_id__in=config.bot.admins).first()
    users = []
    for i in range(250):
        mock_user = mock.Mock()
        mock_user.user_id = user.user_id
        mock_user.first_name = user.first_name
        users.append(mock_user)
    return users


class MailStatus(str, Enum):
    run = "run"
    pause = "pause"
    stop = "stop"


class MailSender(BaseModel):
    status: MailStatus = MailStatus.run
    message: types.Message
    mail: str
    markup: types.InlineKeyboardMarkup | None

    status_markup: types.InlineKeyboardMarkup | None
    status_message: types.Message | None

    quantity: int = 0
    num: int = 0
    success: int = 0
    failure: int = 0

    async def edit_status_message(self):
        percent = 100 // (self.quantity // self.num)
        await self.status_message.edit_text(f"Выполнено {self.num}/{self.quantity} [{percent} %]:\n"
                                            f"✅ Успешно: {self.success}\n"
                                            f"🚫 Неудачно: {self.failure}", reply_markup=self.status_markup)

    async def sending_mail_status(self):
        while self.status is not MailStatus.stop:
            if self.status is MailStatus.run:
                with contextlib.suppress(exceptions.TelegramBadRequest):
                    await self.edit_status_message()
            await asyncio.sleep(1)
        # await self.edit_status_message()

    async def send_mail(self):
        users = await User.exclude(user_id__in=config.bot.admins)
        self.status_markup = markups.admin_menu.send_mail_done()
        self.status_message = await self.message.answer(f"Выполнено {0}/{len(users)}:\n"
                                                        f"Успешно: {0}\n"
                                                        f"Неуспешно: {0}",
                                                        reply_markup=self.status_markup)
        # return
        users = await get_mock_users()
        self.quantity = len(users)
        asyncio.create_task(self.sending_mail_status())
        for num, user in enumerate(users, 1):
            self.num = num
            try:
                while True:
                    if self.status is MailStatus.run:
                        await bot.send_message(user.user_id, self.mail, reply_markup=self.markup)
                        logger.trace(f"Рассылка успешно отправлена пользователю [{user.first_name}]{user.user_id}")
                        self.success += 1
                        break
                    elif self.status is MailStatus.pause:
                        logger.trace(f"Отправка рассылки на паузе")
                        await asyncio.sleep(1)
                    else:
                        logger.trace(f"Рассылка остановлена")
                        self.status_markup = None
                        await self.edit_status_message()
                        return
            except Exception as e:
                self.failure += 1
                logger.warning(e)
            # await self.edit_status_message(num, quantity)

        await self.message.answer(f"Рассылка отправлена всем {self.quantity} пользователям")


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
                logger.trace(e)
                results.append(True)
        return all(results)
    else:
        return True
