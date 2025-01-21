from bot.utils.like_form.create_liked_form import create_liked_form
from bot.utils.like_form.notification_about_like import send_notification_about_like
from bot.other_functions.string_to_list import string_to_list
from database.database_code import Database
from bot.logs.logger import logger

db = Database()


async def process_like(user_id: int, data_to_insert: tuple):
    try:
        current_form_index = db.get_user_value(user_id=user_id,
                                               name="current_form_index")

        forms_row = db.get_user_value(user_id=user_id, name='forms_row')

        # Добавление в БД данных
        create_liked_form(forms_row=forms_row, current_form_index=current_form_index,
                          who_liked_user_id=user_id,
                          other_data=data_to_insert)  # Создаём запись, обращаясь к current_form_id - 1

        # Отправляем тому, кого лайкнули
        liked_form_id = string_to_list(massive=str(forms_row), form_index=current_form_index - 1)
        liked_user_id = db.get_user_id_by_form_id(form_id=liked_form_id)
        await send_notification_about_like(user_id=liked_user_id)

        return forms_row, current_form_index
    except Exception as e:
        logger.error("Возникла ошибка в process_like: %s", e)
