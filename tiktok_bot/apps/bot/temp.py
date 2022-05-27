import typing

if typing.TYPE_CHECKING:
    from tiktok_bot.apps.bot.handlers.utils import MailSender

SUBSCRIPTION_CHANNELS: list[tuple[str, str]] = []
SPONSOR_CHANNELS = []
SPONSOR_CHANNELS_VIEW = 0
MAIL_SENDER: typing.Optional["MailSender"] = None
BOT_RUNNING: bool = True
ONLINE_USERS: dict[int, bool] = {}
TODAY_DOWNLOADS: int = 0
