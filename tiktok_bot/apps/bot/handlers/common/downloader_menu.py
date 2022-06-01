import asyncio

from aiogram import Dispatcher, Router, types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import BufferedInputFile
from aiogram.utils.chat_action import ChatActionSender
from loguru import logger
from tiktok_downloader import snaptik

from tiktok_bot.apps.bot import temp
from tiktok_bot.apps.bot.filters.base_filters import UserFilter, ChannelSubscriptionFilter, something
from tiktok_bot.apps.bot.markups.common import common_markups
from tiktok_bot.db.models import User, AdvUser, SponsorChat

router = Router()


def download_file(video_url) -> bytes:
    video = snaptik(video_url)
    medias = video.get_media()
    filter_media = list(filter(lambda x: not x.watermark, medias))
    media = filter_media[0] if filter_media else medias[0]
    media_bytes = media.download()
    bytes_storage = media_bytes.getvalue()
    return bytes_storage


async def download(message: types.Message, user: User, state: FSMContext):
    await state.clear()
    # todo 5/26/2022 7:59 PM taima: add span detecter
    await user.fetch_related("adv_user")

    if not user.adv_user:
        await AdvUser.create(user=user)
        await user.refresh_from_db()
        await user.fetch_related("adv_user")

    if user.is_search:
        await message.answer("Уже скачивается видео, ожидайте...")
        return

    sponsor_chat = await SponsorChat.all().order_by("id").first()
    async with user:
        try:
            await message.answer("Скачиваю видео, ожидайте...")
            async with ChatActionSender.upload_video(bot=message.via_bot, chat_id=message.chat.id):
                bytes_storage = await asyncio.to_thread(download_file, message.text)
                await message.answer_video(
                    BufferedInputFile(bytes_storage,
                                      filename=f"result_{message.from_user.id}.mp4"),
                    caption="Вот твое видео: скачано с помощью @tiktokksave_bot",
                    reply_markup=common_markups.download(sponsor_chat, message.text))
            await message.answer("Скачиваю музыку из видео...")
            async with ChatActionSender.upload_voice(bot=message.via_bot, chat_id=message.chat.id):
                await message.answer_audio(
                    BufferedInputFile(bytes_storage,
                                      filename=f"result_{message.from_user.id}.mp4"),
                    caption="Вот музыка из видео: скачано с помощью @tiktokksave_bot",
                    reply_markup=common_markups.download_audio())
            temp.TODAY_DOWNLOADS += 1
            temp.SPONSOR_CHANNELS_VIEW += 1
            if sponsor_chat:
                await sponsor_chat.incr_view()
            await user.adv_user.incr_download()
        except Exception as e:
            logger.exception(e)
            await message.answer("Ошибка при скачивании, неверная ссылка, видео было удалено или я его не нашел.")


def register_downloader(dp: Dispatcher):
    dp.include_router(router)

    callback = router.callback_query.register
    message = router.message.register

    message(download, UserFilter(), ChannelSubscriptionFilter(), text_contains="tiktok.com", state="*")
