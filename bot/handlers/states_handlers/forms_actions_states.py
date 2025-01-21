from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from bot.bot_instance import bot
from bot.states.states_initialization import FormActions
from bot.utils.scrolling_utils.process_scroling import process_scrolling
from bot.utils.like_form.create_liked_form import create_liked_form
from bot.utils.like_form.notification_about_like import send_notification_about_like
from bot.utils.like_form.process_like import process_like
from bot.other_functions.string_to_list import string_to_list
from database.database_code import Database
from bot.logs.logger import logger


router = Router()

db = Database()


@router.message(FormActions.get_like_message)
async def get_like_text(message: types.Message, state: FSMContext):
    try:
        if message.text:
            data_to_insert = ("like_text", message.text)
            data_for_next_form = await process_like(user_id=message.chat.id,
                                                    data_to_insert=data_to_insert)  # Отправка лайков
            # Продолжаем скроллинг
            forms_row = data_for_next_form[0]
            current_form_index = data_for_next_form[1]

            await bot.send_message(chat_id=message.chat.id, text='Лайк и сообщение отправлены🩷')
            current_form_id = string_to_list(massive=str(forms_row), form_index=current_form_index)
            await process_scrolling(user_id=message.from_user.id, current_form_id=current_form_id,
                                    current_form_index=current_form_index)  # Новая анкета

            await state.clear()
        else:
            await bot.send_message(chat_id=message.chat.id, text='Отправь мне текст!')
    except Exception as e:
        logger.erro("Возникла ошибка в get_like_text: %s", e)


@router.message(FormActions.get_like_media, F.photo)
async def get_like_media_photo(message: types.Message, state: FSMContext):
    try:
        data_to_insert = ("like_photo", message.photo[-1].file_id)
        data_for_next_form = await process_like(user_id=message.chat.id,
                                                data_to_insert=data_to_insert)  # Отправка лайков

        # Продолжаем скроллинг
        forms_row = data_for_next_form[0]
        current_form_index = data_for_next_form[1]

        await bot.send_message(chat_id=message.chat.id, text='Лайк и фото отправлены🩷')

        current_form_id = string_to_list(massive=str(forms_row), form_index=current_form_index)
        await process_scrolling(user_id=message.from_user.id, current_form_id=current_form_id,
                                current_form_index=current_form_index)  # Новая анкета

        await state.clear()
    except Exception as e:
        logger.error("Возникла ошибка в get_like_media_photo: %s", e)


@router.message(FormActions.get_like_media, F.video)
async def get_like_media_video(message: types.Message, state: FSMContext):
    try:
        data_to_insert = ("like_video", message.video.file_id)

        data_for_next_form = await process_like(user_id=message.chat.id,
                                                data_to_insert=data_to_insert)  # Отправка лайков

        # Продолжаем скроллинг
        forms_row = data_for_next_form[0]
        current_form_index = data_for_next_form[1]

        await bot.send_message(chat_id=message.chat.id, text='Лайк и видео отправлены🩷')

        current_form_id = string_to_list(massive=str(forms_row), form_index=current_form_index)
        await process_scrolling(user_id=message.from_user.id, current_form_id=current_form_id,
                                current_form_index=current_form_index)

        await state.clear()
    except Exception as e:
        logger.error("Возникла ошибка в get_like_media_video: %s", e)


@router.message(FormActions.get_like_media, F.text)
async def get_like_media_wrong(message: types.Message):
    try:
        await bot.send_message(chat_id=message.chat.id, text='Отправь мне фото или видео!')
    except Exception as e:
        logger.error("Возникла ошибка в get_like_media_wrong: %s", e)


@router.message(FormActions.get_like_voice)
async def get_like_voice(message: types.Message, state: FSMContext):
    try:
        if message.voice:
            data_to_insert = ("like_voice", message.voice.file_id)
            data_for_next_form = await process_like(user_id=message.chat.id,
                                                    data_to_insert=data_to_insert)  # Отправка лайков

            # Продолжаем скроллинг
            forms_row = data_for_next_form[0]
            current_form_index = data_for_next_form[1]

            await bot.send_message(chat_id=message.chat.id, text='Лайк и голосовое сообщение отправлены🩷')

            current_form_id = string_to_list(massive=str(forms_row), form_index=current_form_index)
            await process_scrolling(user_id=message.from_user.id, current_form_id=current_form_id,
                                    current_form_index=current_form_index)

            await state.clear()
        else:
            await bot.send_message(chat_id=message.chat.id, text="Отправь мне голосовое сообщение!")
    except Exception as e:
        logger.error("Возникла ошибка в get_like_voice: %s", e)
