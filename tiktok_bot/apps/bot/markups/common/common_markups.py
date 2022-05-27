from tiktok_bot.apps.bot.markups.utils import get_inline_keyboard, get_as_column, get_inline_button, \
    get_inline_url_keyboard, get_reply_keyboard
from tiktok_bot.db.models import SponsorChat
from tiktok_bot.loader import _


def start_menu():
    keyboard = [
        ((_("👤 Мой профиль"), "profile"),),
    ]
    return get_inline_keyboard(keyboard)


def download(sponsor_chat: SponsorChat, url: str):
    keyboard = [
        (("Поделиться", url),),
        ((sponsor_chat.skin, sponsor_chat.link),) if sponsor_chat else []
    ]
    return get_inline_url_keyboard(keyboard)


def download_audio():
    keyboard = [
        ["🔍 История"]
    ]
    return get_reply_keyboard(keyboard)


def channel_status_check(channels: list[tuple[str, str]]):
    keyboard = []
    for num, skin in enumerate(channels, 1):
        keyboard.append(
            (f"Канал #{num}", f"https://t.me/{skin[1][1:]}"),
        )
    column_keyboard = get_as_column(keyboard)
    ikeyboard = get_inline_url_keyboard(column_keyboard)
    inline_button = get_inline_button(("✅ Я подписался", "start"))
    ikeyboard.inline_keyboard.append([inline_button])
    return ikeyboard
