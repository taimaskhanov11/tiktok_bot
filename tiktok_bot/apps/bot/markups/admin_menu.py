from tiktok_bot.apps.bot.callback_data.base_callback import ChatCallback
from tiktok_bot.apps.bot.markups.utils import get_inline_keyboard


def admin_start():
    keyword = [
        (("👥 Узнать количество пользователей.", "users_count"),),
        (("📄 Список каналов и групп для подписки.", ChatCallback(pk=0, action="view").pack()),),
        (("✍ Добавить канал для подписки.", ChatCallback(pk=0, action="new").pack()),),
        (("🔖 Сделать рассылку.", "send_mail"),),
        # (("📋 Стартовое сообщение", "start_message"),),
    ]

    return get_inline_keyboard(keyword)


def view_chats(chats):
    keyboard = (
        ((c.link, ChatCallback(pk=c.pk, action="touch").pack(),) for c in chats),
    )
    return get_inline_keyboard(keyboard)


def touch_chat(chat):
    keyboard = [
        (("✍ Удалить.", ChatCallback(pk=chat.pk, action="delete").pack()), ),
    ]
    return get_inline_keyboard(keyboard)


def admin_button():
    keyboard = [
        (("Админ панель", "admin"),),
    ]
    return get_inline_keyboard(keyboard)


def start_message():
    keyboard = [
        (("Изменить", "edit_start_message"),),
    ]
    return get_inline_keyboard(keyboard)
