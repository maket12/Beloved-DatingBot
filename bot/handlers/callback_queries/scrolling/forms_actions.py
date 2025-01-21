import asyncio
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from database.database_code import Database
from bot.logs.logger import logger
from bot.bot_instance import bot
from bot.states.states_initialization import FormActions
from bot.handlers.messages.start import start
from bot.utils.scrolling_utils.process_scroling import process_scrolling
from bot.other_functions.string_to_list import string_to_list
from bot.utils.like_form.create_liked_form import create_liked_form
from bot.utils.like_form.notification_about_like import send_notification_about_like

router = Router()

db = Database()


@router.callback_query(F.data == "forms_action_like")
async def forms_action_like(call: types.CallbackQuery):
    try:
        current_form_index = db.get_user_value(user_id=call.from_user.id, name="current_form_index")

        forms_row = db.get_user_value(user_id=call.from_user.id, name='forms_row')

        create_liked_form(forms_row=forms_row, current_form_index=current_form_index,
                          who_liked_user_id=call.from_user.id)  # Создаём запись, обращаясь к current_form_id - 1

        # Оповещаем пользователя о том, что его лайкнули:
        liked_form_id = string_to_list(massive=str(forms_row), form_index=current_form_index-1)  # Текущая анкета
        liked_user_id = db.get_user_id_by_form_id(form_id=liked_form_id)
        await send_notification_about_like(user_id=liked_user_id)

        await bot.edit_message_text(text='Лайк отправлен🩷', chat_id=call.from_user.id,
                                    message_id=call.message.message_id)

        await asyncio.sleep(1.2)

        current_form_id = string_to_list(massive=str(forms_row), form_index=current_form_index)
        await process_scrolling(user_id=call.from_user.id, current_form_id=current_form_id,
                                current_form_index=current_form_index)
    except Exception as e:
        logger.error('Возникла ошибка в forms_action_like: %s', e)


@router.callback_query(F.data == "forms_action_dislike")
async def forms_action_dislike(call: types.CallbackQuery):
    try:
        current_form_index = db.get_user_value(user_id=call.from_user.id, name="current_form_index")

        forms_row = db.get_user_value(user_id=call.from_user.id, name='forms_row')
        current_form_id = string_to_list(massive=str(forms_row), form_index=current_form_index)

        await bot.edit_message_text(text='Анкета пропущена', chat_id=call.from_user.id,
                                    message_id=call.message.message_id)

        await asyncio.sleep(1.2)

        await process_scrolling(user_id=call.from_user.id, current_form_id=current_form_id,
                                current_form_index=current_form_index)
    except Exception as e:
        logger.error("Вознилка ошибка в forms_action_dislike: %s", e)


@router.callback_query(F.data == "forms_action_text")
async def forms_action_text(call: types.CallbackQuery, state: FSMContext):
    try:
        await bot.edit_message_text(text='Отправь текст, который надо прислать:',
                                    chat_id=call.from_user.id, message_id=call.message.message_id)
        await state.set_state(FormActions.get_like_message)
    except Exception as e:
        logger.error("Возникла ошибка в forms_action_text: %s", e)


@router.callback_query(F.data == "forms_action_media")
async def forms_action_media(call: types.CallbackQuery, state: FSMContext):
    try:
        await bot.edit_message_text(text='Отправь фото или видео, которое надо прислать:',
                                    chat_id=call.from_user.id, message_id=call.message.message_id)
        await state.set_state(FormActions.get_like_media)
    except Exception as e:
        logger.error("Возникла ошибка в forms_action_media: %s", e)


@router.callback_query(F.data == "forms_action_voice")
async def forms_action_voice(call: types.CallbackQuery, state: FSMContext):
    try:
        check_premium = db.get_user_value(user_id=call.from_user.id, name="is_premium")
        if not check_premium:
            await call.answer(text='Отправка голосового сообщения доступна только с 👑Premium👑!',
                              show_alert=True)
        else:
            await bot.send_message(chat_id=call.from_user.id,
                                   text='Отправь мне голосовое сообщение, которое надо прислать:')
            await state.set_state(FormActions.get_like_voice)
    except Exception as e:
        logger.error("Возникла ошибка в forms_action_voice: %s", e)


@router.callback_query(F.data == "forms_action_complaint")
async def forms_action_complaint(call: types.CallbackQuery, state: FSMContext):
    try:
        await call.answer(text='Данная функция сейчас недоступна😔',
                          show_alert=True)
    except Exception as e:
        logger.error("Возникла ошибка в forms_action_complaint: %s", e)


@router.callback_query(F.data == "forms_action_back")
async def forms_action_back(call: types.CallbackQuery):
    try:
        current_form_index = db.get_user_value(user_id=call.from_user.id, name="current_form_index")

        db.set_user_value(user_id=call.from_user.id, current_form_index=current_form_index-1)

        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await start(message=call)
    except Exception as e:
        logger.error("Возникла ошибка в forms_action_back: %s", e)
