from aiogram import Router, types, F
from bot.bot_instance import bot
from database.database_code import Database
from bot.logs.logger import logger
from bot.utils.scrolling_utils.forms_queue import do_forms_queue
from bot.utils.scrolling_utils.process_scroling import process_scrolling
from bot.other_functions.string_to_list import string_to_list


router = Router()

db = Database()


@router.callback_query(F.data == 'start_scrolling')
async def start_scrolling(call: types.CallbackQuery):
    try:
        await bot.delete_message(call.from_user.id, call.message.message_id)

        current_list_of_forms = db.get_user_value(user_id=call.from_user.id, name='forms_row')

        if not bool(current_list_of_forms):
            # Составляем список анкет, если его нет
            current_list_of_forms = await do_forms_queue(user_id=call.from_user.id)

        current_form_index = db.get_user_value(call.from_user.id,
                            'current_form_index')  # Определяем предыдущую просмотренную анкету

        if not bool(current_form_index):
            current_form_index = 0  # Индекс анкеты в списке forms_row

            db.set_user_value(user_id=call.from_user.id,
                              current_form_index=current_form_index)  # Обновляем БД

        current_form_id = string_to_list(massive=str(current_list_of_forms),
                                form_index=int(current_form_index))  # Берём первую анкету из списка

        await process_scrolling(user_id=call.from_user.id, current_form_id=current_form_id,
                                current_form_index=current_form_index)
    except Exception as e:
        logger.error('Возникла ошибка при старте скроллинга %s', e)