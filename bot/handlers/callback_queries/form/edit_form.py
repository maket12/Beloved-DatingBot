from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from bot.bot_instance import bot
from bot.logs.logger import logger
from bot.keyboards.buttons import edit_form_markup, edit_media_markup, form_settings_markup
from bot.states.states_initialization import FormEdit, FormBuilder
from database.database_code import Database


router = Router()


db = Database()


@router.callback_query(F.data == "edit_form")
async def edit_form(call: types.CallbackQuery):
    try:
        await bot.edit_message_text(text='Выбери, что ты хочешь изменить:', chat_id=call.from_user.id,
                                    message_id=call.message.message_id, reply_markup=edit_form_markup)
    except Exception as e:
        logger.error('Возникла ошибка в edit_form: %s', e)


@router.callback_query(F.data.startswith("edit_form_"))
async def edit_form_parameter(call: types.CallbackQuery, state: FSMContext):
    try:
        parameter = call.data.split('_')[-1]

        if parameter == 'text':
            await bot.edit_message_text(text="Хорошо, отправь мне текст анкеты\n"
                                             "Расскажи о себе, чем любишь заниматься, о своих интересах:",
                                        chat_id=call.from_user.id, message_id=call.message.message_id,
                                        reply_markup=None)
            await state.set_state(FormEdit.edit_form_text)

        elif parameter == 'media':
            await bot.edit_message_text(text="Выбери, что необходимо изменить:", chat_id=call.from_user.id,
                                        message_id=call.message.message_id, reply_markup=edit_media_markup)
        elif parameter == 'again':
            db.delete_form(user_id=call.from_user.id)  # Удаляем анкету пользователя
            db.add_user(user_id=call.from_user.id)  # Вновь добавляем его в БД

            await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
            await bot.send_message(chat_id=call.from_user.id, text='Отлично, давай начнём.\n'
                                                                   'Как тебя зовут?')

            await state.set_state(FormBuilder.create_form_name)  # Начинаем заполнять заново

        else:
            await bot.edit_message_text(text='Всё верно?', chat_id=call.from_user.id,
                                        message_id=call.message.message_id,
                                        reply_markup=form_settings_markup)
    except Exception as e:
        logger.error('Возникла ошибка в edit_form_parameter: %s', e)


@router.callback_query(F.data.startswith("media"))
async def edit_media(call: types.CallbackQuery, state: FSMContext):
    try:
        action = call.data.split('_')[-1]

        if action == 'add':
            await bot.edit_message_text(text='Хорошо, отправь мне фото или видео:', chat_id=call.from_user.id,
                                        message_id=call.message.message_id)
            await state.set_state(FormEdit.edit_form_media)
        elif action == 'delete':
            await call.answer('Данная функция сейчас недоступна и будет добавлена в ближайшем обновлении!',
                              show_alert=True)
        else:
            await edit_form(call=call)  # Возвращаем предыдущую функцию

    except Exception as e:
        logger.error('Возникла ошибка в edit_media: %s', e)
