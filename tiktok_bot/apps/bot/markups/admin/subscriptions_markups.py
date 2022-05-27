from tiktok_bot.apps.bot.callback_data.base_callback import ChatCallback, SponsorChatCallback
from tiktok_bot.apps.bot.markups.utils import get_inline_keyboard, get_as_column
from tiktok_bot.db.models import Chat


def view_chats(chats: list[Chat]):
    keyboard = (
        ((f"{c}", ChatCallback(pk=c.pk, action="touch").pack(),) for c in chats),
    )
    return get_inline_keyboard(keyboard)


def touch_chat(chat):
    keyboard = [
        (("✍ Удалить.", ChatCallback(pk=chat.pk, action="delete").pack()),),
    ]
    return get_inline_keyboard(keyboard)


def sponsor_view_chats(chats):
    keyboard = [
        [f"❌#{num}", SponsorChatCallback(pk=c.pk, action="delete").pack(), ] for num, c in enumerate(chats)
    ]
    return get_inline_keyboard(get_as_column(keyboard))


def sponsor_touch_chat(chat):
    keyboard = [
        (("✍ Удалить.", SponsorChatCallback(pk=chat.pk, action="delete").pack()),),
    ]
    return get_inline_keyboard(keyboard)
