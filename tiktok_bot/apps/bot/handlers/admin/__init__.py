from aiogram import Dispatcher, Router, F

from tiktok_bot.config.config import config
from .admin_menu import register_admin
from .send_mail_handers import register_send_mail

router = Router()


def register_admin_handlers(dp: Dispatcher):
    router.message.filter(F.from_user.id.in_(config.bot.admins))
    router.callback_query.filter(F.from_user.id.in_(config.bot.admins))
    register_admin(router)
    register_send_mail(router)
    dp.include_router(router)
