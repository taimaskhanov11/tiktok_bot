from aiogram.dispatcher.filters.callback_data import CallbackData


# todo 5/13/2022 3:17 PM taima: добавить Enum
class UserCallback(CallbackData, prefix="user"):
    pk: int
    action: str


# class Action(str, Enum):
#     view = "view"
#     new = "new"


class ChatCallback(CallbackData, prefix="chat"):
    pk: int
    action: str


class SponsorChatCallback(CallbackData, prefix="sponsor_chat"):
    pk: int
    action: str
