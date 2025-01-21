from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from bot.bot_instance import bot
from bot.keyboards.buttons import form_settings_markup
from bot.states.states_initialization import FormEdit
from bot.utils.send_form_utils.send_form import send_form
from database.database_code import Database
from bot.logs.logger import logger


router = Router()

db = Database()


@router.message(FormEdit.edit_form_text)
async def get_new_text(message: types.Message, state: FSMContext):
    try:
        if message.text:
            db.set_user_value(user_id=message.chat.id, profile_text=message.text)

            await bot.send_message(chat_id=message.chat.id, text='Отлично, анкета обновлена!')

            await send_form(user_id=message.chat.id, other_form_flag=False)
            await bot.send_message(chat_id=message.chat.id, text='Всё верно?', reply_markup=form_settings_markup)

            await state.clear()
        else:
            await bot.send_message(chat_id=message.chat.id, text='Отправь мне текст анкеты: ')
    except Exception as e:
        logger.error('Возникла ошибка в get_new_text %s', e)
        await state.clear()


@router.message(FormEdit.edit_form_media)
async def add_new_media(message: types.Message, state: FSMContext):
    try:
        current_file_ids = db.get_user_value(message.chat.id, 'profile_media')

        if message.photo:
            file_id = message.photo[-1].file_id
        elif message.video:
            file_id = message.video.file_id
        else:
            await bot.send_message(chat_id=message.chat.id, text='Отправь фото или видео!')
            return

        if bool(current_file_ids):
            current_file_ids += '|' + file_id
        else:
            current_file_ids = file_id

        db.set_user_value(user_id=message.chat.id, profile_media=current_file_ids)

        await bot.send_message(chat_id=message.chat.id, text='Отлично, анкета обновлена!')

        await send_form(user_id=message.chat.id, other_form_flag=False)  # Отправляем анкету
        await bot.send_message(chat_id=message.chat.id, text='Всё верно?', reply_markup=form_settings_markup)

        await state.clear()
    except Exception as e:
        logger.error('Возникла ошибка в add_new_media %s', e)
        await state.clear()
