from tiktok_bot.apps.bot.markups.utils import get_inline_keyboard

back_buttons = [
    (("⬅ Назад", "statistics"),),
]


def statistics_start():
    keyword = [
        (("👥 Узнать количество пользователей.", "users_count"),),
        (("👥 Количество новых пользователей за сегодня.", "users_count_new"),),
        (("👥 Количество пользователей онлайн.", "users_count_online"),),
    ]

    return get_inline_keyboard(keyword)


def back():
    return get_inline_keyboard(back_buttons)
