import re
from pprint import pprint

from aiogram.types import InlineKeyboardMarkup
from loguru import logger

from tiktok_bot.apps.bot.callback_data.base_callback import ChatCallback
from tiktok_bot.apps.bot.markups.utils import get_inline_keyboard, get_inline_url_keyboard


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
        (("✍ Удалить.", ChatCallback(pk=chat.pk, action="delete").pack()),),
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


def send_mail_preview():
    keyboard = [
        (("➕ Добавить url кнопки", "add_button"),),
        (("✅ Подтвердить", "accept"),),
        (("❌ Отменить", "admin"),),
        # (("❌ Отменить", "cancel"),),
    ]
    return get_inline_keyboard(keyboard)


def send_mail_done(status: bool = True):
    keyboard = [
        (("⏸ Пауза", "pause_mail"),) if status else (("▶️ Возобновить", "continue_mail"),),
        (("⏹ Стоп", "stop_mail"),),
    ]
    return get_inline_keyboard(keyboard)


@logger.catch
def parse_buttons(text: str):
    keyboard = []
    change_keyboard = re.split(r'\s\n|\w\n|$', text)[:-1]
    for but_parent in change_keyboard:
        keyboard.append(
            list(map(lambda x: list(map(lambda x: x.strip(), x.split('-'))), but_parent.split("|\n")))
        )
    return keyboard
    # return get_inline_url_keyboard(keyboard)
    # data = re.findall(r"(\bwall|\bphoto)(-?\d+_\d+)", i)


def send_mail_add_button(text: str) -> InlineKeyboardMarkup:
    keyboard = [
        # (("➕ Добавить еще url кнопки", "add_button"),),
        (("➕ Добавить новый url кнопки", "add_button"),),
        (("✅ Подтвердить", "accept"),),
        (("❌ Отменить", "cancel"),),
    ]
    inline_keyboard = get_inline_keyboard(keyboard)
    inline_url_keyboard = get_inline_url_keyboard(parse_buttons(text))
    inline_url_keyboard.inline_keyboard.extend(inline_keyboard.inline_keyboard)
    return inline_url_keyboard


if __name__ == '__main__':
    text = ("Кнопка 1 - https://www.example1.com |\n"
            "Кнопка 2 - https://www.example2.com |\n"
            "Кнопка 3 - https://www.example3.com \n"
            "Кнопка 4 - https://www.example4.com")
    # pprint(send_mail_preview().inline_keyboard)
    pprint(parse_buttons(text))
    # print(send_mail_add_button(text))
    # parse_buttons("Кнопка 1 - https://www.example1.com,\n"
    #               "Кнопка 2 - https://www.example2.com,\n"
    #               "Кнопка 3 - https://www.example3.com|\n"
    #               "Кнопка 4 - https://www.example4.com\n")
