from bot.other_functions.string_to_list import string_to_list
from database.database_code import Database
from bot.logs.logger import logger

db = Database()


def create_liked_form(forms_row: str, current_form_index: int, who_liked_user_id: int, other_data=None):
    try:
        form_id = string_to_list(massive=str(forms_row), form_index=current_form_index-1)  # Предыдущая по списку

        who_liked_form_id = db.get_user_value(user_id=who_liked_user_id, name="id")

        db.add_liked_form(form_id=form_id, who_liked_form_id=who_liked_form_id,
                          other_data=other_data)
    except Exception as e:
        logger.error("Возникла ошибка в create_liked_form: %s", e)
