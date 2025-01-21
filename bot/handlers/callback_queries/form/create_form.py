from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from bot.states.states_initialization import FormBuilder
from bot.bot_instance import bot
from bot.keyboards.buttons import create_edit_media_markup, goals_of_form_markup, my_gender_markup, they_gender_markup
from bot.logs.logger import logger
from database.database_code import Database


router = Router()

db = Database()


@router.callback_query(F.data == 'create_form')
async def start_create_form(call: types.CallbackQuery, state: FSMContext):
    try:
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.send_message(call.from_user.id, text='Отлично, давай начнём.\nКак тебя зовут?')
        await state.set_state(FormBuilder.create_form_name)
    except Exception as e:
        logger.error('Возникла ошибка при создании анкеты: %s', e)
    finally:
        db.add_user(call.from_user.id)


@router.callback_query(F.data.startswith('create_form_add_'))
async def add_media(call: types.CallbackQuery, state: FSMContext):
    try:
        existing_medias = db.get_user_value(call.from_user.id, "profile_media")
        if len(existing_medias.split('|')) < 3:
            media_type = call.data.split('_')[3]
            if media_type == 'photo':
                await bot.edit_message_text(text='Отправь мне фото, которое необходимо добавить:',
                                            chat_id=call.from_user.id,
                                            message_id=call.message.message_id)
            else:
                await bot.edit_message_text(text='Отправь мне видео, которое необходимо добавить:',
                                            chat_id=call.from_user.id,
                                            message_id=call.message.message_id)
            await state.set_state(FormBuilder.create_form_media)
        else:
            await bot.edit_message_text(text='Ты уже добавил максимально возможное количество медиа\n'
                                        'Можем переходить к следующему шагу',
                                        chat_id=call.from_user.id,
                                        message_id=call.message.message_id,
                                        reply_markup=await create_edit_media_markup(3))
    except Exception as e:
        logger.error('Возникла ошибка при создании анкеты: %s', e)


@router.callback_query(F.data == 'complete_add_media')
async def complete_add_media(call: types.CallbackQuery):
    try:
        await bot.delete_message(call.from_user.id, call.message.message_id)

        checking = db.get_user_value(call.from_user.id, "profile_media")

        if not bool(checking):
            await bot.send_message(call.from_user.id, 'Необходимо добавить как минимум 1 медиа!',
                                   reply_markup=await create_edit_media_markup(1))  # Не важно какое кол-во указывать

        else:
            await bot.send_message(call.from_user.id,
                                   'Теперь выбери цель создания анкеты.\n'
                                   'Это поможет лучше подобрать тебе анкеты:',
                                   reply_markup=goals_of_form_markup)
    except Exception as e:
        logger.error('Возникла ошибка при создании анкеты: %s', e)


@router.callback_query(F.data.startswith('goal'))
async def get_form_goal(call: types.CallbackQuery, state: FSMContext):
    goals_dict = {
        "love": "💕Отношения💕",
        "friends": "🤝Дружба🤝",
        "chatting": "💬Общение💬",
        "nothing": "🤷Без разницы🤷"
    }

    try:
        goal = call.data.split('_')[1]
        goal_in_russian = goals_dict[goal]

        await state.update_data(profile_goal=goal_in_russian)

        await bot.edit_message_text(text='Хорошо, теперь укажи свой пол:', chat_id=call.from_user.id,
                                    message_id=call.message.message_id,
                                    reply_markup=my_gender_markup)
    except Exception as e:
        logger.error('Возникла ошибка при создании анкеты: %s', e)


@router.callback_query(F.data.startswith('my_gender'))
async def get_gender(call: types.CallbackQuery, state:FSMContext):
    try:
        gender = call.data.split('_')[-1]
        await state.update_data(self_gender=gender)
        await bot.edit_message_text(text='Хорошо, теперь укажи пол того, кого хочешь искать:',
                                    chat_id=call.from_user.id,
                                    message_id=call.message.message_id,
                                    reply_markup=they_gender_markup)
    except Exception as e:
        logger.error('Возникла ошибка при создании анкеты: %s', e)
        await state.clear()


@router.callback_query(F.data.startswith('they_gender'))
async def get_they_gender(call: types.CallbackQuery, state: FSMContext):
    try:
        gender = call.data.split('_')[-1]
        if gender == 'any':
            gender = 'male female'

        await state.update_data(find_gender=gender)

        await bot.edit_message_text(
            text='Осталось совсем немного!\nТеперь добавим текст в твою анкету\n'
            'Расскажи о себе, опиши то, чем любишь заниматься',
            chat_id=call.from_user.id, message_id=call.message.message_id)

        await state.set_state(FormBuilder.create_form_profile_text)
    except Exception as e:
        logger.error('Возникла ошибка при создании анкеты: %s', e)
        await state.clear()
