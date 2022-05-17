import asyncio

from aiogram import Dispatcher, Router, types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import BufferedInputFile
from loguru import logger
from tiktok_downloader import snaptik

from tiktok_bot.apps.bot.filters.base_filters import UserFilter
from tiktok_bot.db.models import User

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
    if user.is_search:
        await message.answer("Ожидайте загрузки предыдущего видео...")
        return

    async with user:
        try:
            await message.answer("Скачиваю видео...")
            await message.answer("Ожидайте...")
            bytes_storage = await asyncio.to_thread(download_file, message.text)
            await message.answer_video(
                BufferedInputFile(bytes_storage,
                                  filename=f"result_{message.from_user.id}.mp4"),
                caption="Вот твое видео: скачано с помощью @tiktokksave_bot")

            await message.answer("Скачиваю музыку из видео...")
            await message.answer_audio(
                BufferedInputFile(bytes_storage,
                                  filename=f"result_{message.from_user.id}.mp4"),
                caption="Вот музыка из видео: скачано с помощью @tiktokksave_bot")
        except Exception as e:
            logger.error(e)
            await message.answer("Ошибка при скачивании, неверная ссылка, видео было удалено или я его не нашел.")


def register_downloader(dp: Dispatcher):
    dp.include_router(router)

    callback = router.callback_query.register
    message = router.message.register

    message(download, UserFilter(), text_contains="tiktok.com", state="*")
