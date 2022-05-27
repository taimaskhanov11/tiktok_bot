import datetime

from loguru import logger

from tiktok_bot.apps.bot import temp
from tiktok_bot.apps.bot.temp import ONLINE_USERS
from tiktok_bot.db.models import Chat
from tiktok_bot.loader import scheduler


async def init_chats():
    logger.info("Initial chats")
    # for chat in *await Chat.all(), *await SponsorChat.all():
    for chat in await Chat.all():
        chat.add_to_temp()


def run_user_online_status_deleter(user_id):
    new_date = datetime.datetime.now() + datetime.timedelta(minutes=3)
    scheduler.add_job(lambda x: ONLINE_USERS.pop(user_id),
                      "date",
                      run_date=new_date,
                      args=[user_id])


@scheduler.scheduled_job('cron', hour=0)
def reset_download_count():
    temp.TODAY_DOWNLOADS = 0
