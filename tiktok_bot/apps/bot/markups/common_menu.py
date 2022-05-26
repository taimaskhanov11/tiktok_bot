from tiktok_bot.apps.bot.markups.utils import get_inline_keyboard
from tiktok_bot.loader import _


def start_menu():
    keyboard = [
        ((_("👤 Мой профиль"), "profile"),),
    ]
    return get_inline_keyboard(keyboard)
