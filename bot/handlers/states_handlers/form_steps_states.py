from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from bot.bot_instance import bot
from bot.keyboards.buttons import create_edit_media_markup, geolocation_markup, form_settings_markup
from bot.states.states_initialization import FormBuilder
from bot.utils.send_form_utils.send_form import send_form
from database.database_code import Database
from bot.logs.logger import logger


router = Router()


db = Database()


@router.message(FormBuilder.create_form_name)
async def create_form_step_1(message: types.Message, state: FSMContext):
    try:
        await state.update_data(name=message.text)
        await bot.send_message(message.chat.id, 'Хорошо, теперь укажи свой возраст:')
        await state.set_state(FormBuilder.create_form_age)
    except Exception as e:
        logger.error('Возникла ошибка при создании анкеты: %s', e)


@router.message(FormBuilder.create_form_age)
async def create_form_step_2(message: types.Message, state: FSMContext):
    try:
        if message.text.isdigit():
            state_data = await state.get_data()
            name = state_data["name"]

            db.set_user_value(user_id=message.chat.id, name=name, age=message.text)

            await bot.send_message(message.chat.id,
                                   'У тебя прекрасный возраст♥️\nТеперь добавь в свою анкету фото или видео\n'
                                   '🗂Сейчас прикреплено 0/3 фото', reply_markup=await create_edit_media_markup(1))
            await state.clear()
        else:
            await bot.send_message(message.chat.id, 'Необходимо отправить число, а не текст!')
    except Exception as e:
        logger.error('Возникла ошибка при создании анкеты: %s', e)


@router.message(FormBuilder.create_form_media)
async def get_media_for_form(message: types.Message, state: FSMContext):
    try:
        await bot.delete_message(message.chat.id, message.message_id - 1)

        current_file_ids = db.get_user_value(message.chat.id, 'profile_media')

        if message.photo:
            file_id = message.photo[-1].file_id
        elif message.video:
            file_id = message.video.file_id
        else:
            await bot.send_message(chat_id=message.chat.id, text='Отправь фото или видео!')
            return

        if not bool(current_file_ids):
            current_file_ids += file_id
        else:
            current_file_ids += '|' + file_id
        db.set_user_value(user_id=message.chat.id, profile_media=current_file_ids)

        media_count = len(current_file_ids.split('|'))
        await bot.send_message(message.chat.id, f'Медиа добавлено\n🗂Сейчас прикреплено {media_count}/3 фото',
                               reply_markup=await create_edit_media_markup(media_count))
        await state.clear()
    except Exception as e:
        logger.error('Возникла ошибка при создании анкеты: %s', e)


@router.message(FormBuilder.create_form_profile_text)
async def create_form_step_4(message: types.Message, state: FSMContext):
    try:
        await state.update_data(profile_text=message.text)
        await bot.send_message(message.chat.id, 'Теперь укажи свой город:')
        await state.set_state(FormBuilder.create_form_city)
    except Exception as e:
        logger.error('Возникла ошибка при создании анкеты: %s', e)


@router.message(FormBuilder.create_form_city)
async def create_form_step_5(message: types.Message, state: FSMContext):
    try:
        await state.update_data(city=message.text.lower().capitalize())
        await bot.send_message(message.chat.id,
                               'Отправь мне свою геолокацию📍\n'
                               'Это нужно, чтобы подобрать тебе людей поблизости',
                               reply_markup=geolocation_markup)
        await state.set_state(FormBuilder.create_form_geolocation)
    except Exception as e:
        logger.error('Возникла ошибка при создании анкеты: %s', e)


@router.message(FormBuilder.create_form_geolocation)
async def create_form_step_6(message: types.Message, state: FSMContext):
    try:
        await bot.delete_message(message.chat.id, message.message_id - 1)
        await bot.delete_message(message.chat.id, message.message_id)
        if message.content_type == 'location':
            latitude = message.location.latitude
            longitude = message.location.longitude
            form_geolocation = str(latitude) + '|' + str(longitude)
        else:
            form_geolocation = ""

        state_data = await state.get_data()

        form_goal = state_data["profile_goal"]
        form_self_gender = state_data["self_gender"]
        form_they_gender = state_data["find_gender"]
        form_text = state_data["profile_text"]
        form_city = state_data["city"]

        db.set_user_value(user_id=message.chat.id, profile_goal=form_goal, self_gender=form_self_gender,
                          find_gender=form_they_gender, profile_text=form_text, city=form_city,
                          geolocation=form_geolocation)  # Устанавливаем все параметры анкеты

        await bot.send_message(message.chat.id, '✅')

        await send_form(user_id=message.chat.id, other_form_flag=False)
        await bot.send_message(message.chat.id, 'Всё верно?', reply_markup=form_settings_markup)
    except Exception as e:
        logger.error('Возникла ошибка при создании анкеты: %s', e)
    finally:
        await state.clear()
