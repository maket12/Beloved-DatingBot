from bot.bot_instance import bot
from bot.utils.send_form_utils.send_form import send_form
from bot.keyboards.buttons import forms_actions_markup
from bot.logs.logger import logger
from database.database_code import Database

db = Database()


# Формирование анкеты
async def create_form(user_id: int, form_id: int):
    try:
        if not form_id:
            await bot.send_message(chat_id=user_id, text="Кажется, больше нет подходящих анкет😕\n"
                                                         "Подождём, пока тебя кто-то лайкнет")
            return
        form_user_id = db.get_user_id_by_form_id(form_id=form_id)
        await send_form(user_id=user_id, form_user_id=form_user_id)  # Отправляем анкету

        await bot.send_message(chat_id=user_id, text='⬆️Выбери действие для анкеты⬆️',
                               reply_markup=forms_actions_markup)
    except Exception as e:
        logger.error('Возникла ошибка в process_scrolling: %s', e)
        logger.info(form_id)


async def process_scrolling(user_id: int, current_form_id: int, current_form_index: int):
    try:
        await create_form(user_id=user_id, form_id=current_form_id)

        db.set_user_value(user_id=user_id, current_form_index=current_form_index+1)  # Следующая анкета по списку
    except Exception as e:
        logger.error('Возникла ошибка в process_scrolling: %s', e)
