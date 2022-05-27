from tiktok_bot.apps.bot import temp
from tiktok_bot.apps.bot.markups.utils import get_inline_keyboard


def bot_setting_start():
    keyboard = [
        (("🚫 Приостановить", "stop_bot"),) if temp.BOT_RUNNING else (("▶ Запустить", "run_bot"),),
        (("🔃 Перезапустить", "restart_bot"),),
        (("⬅️ Назад", "admin"),),
    ]
    return get_inline_keyboard(keyboard)
