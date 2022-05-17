from typing import Generator

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup


def get_inline_button(bnt_data):
    return InlineKeyboardButton(text=bnt_data[0], callback_data=bnt_data[1])


def get_inline_url_button(bnt_data):
    return InlineKeyboardButton(text=bnt_data[0], url=bnt_data[1])


# todo 5/13/2022 5:39 PM taima: change to tuple or frozenset
def get_inline_keyboard(ikm_data: list[tuple | Generator] | Generator):
    inline_keyboard = [list(map(get_inline_button, btn)) for btn in ikm_data]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def get_inline_url_keyboard(ikm_data: list[tuple] | Generator):
    inline_keyboard = [list(map(get_inline_url_button, btn)) for btn in ikm_data]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def get_keyboard(km_data: list[tuple[str]]):
    return ReplyKeyboardMarkup()
