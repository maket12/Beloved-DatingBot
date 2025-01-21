from database.database_code import Database
from bot.logs.logger import logger


db = Database()


# Функция создания анкеты в текстовом виде
async def create_form_txt(user_id: int, other_form_flag: bool, is_mutual_like: bool):
    text_of_form = ''
    try:
        form_data = db.get_users_form(user_id=user_id)
        name = form_data[2]
        age = form_data[3]
        city = form_data[9]
        profile_goal = form_data[7]
        profile_text = form_data[8]
        premium_flag = form_data[13]

        if premium_flag:
            text_of_form = '👑Premium👑\n'

        text_of_form += (f'{name.capitalize()}, {age}, {city}\n'
                         f'Цель: {profile_goal}\n'
                         f'{profile_text}')
        if is_mutual_like:
            text_of_form = 'Есть взаимная симпатия💕:\n' + text_of_form
        if not other_form_flag:
            text_of_form = 'Вот твоя анкета:\n' + text_of_form
        # else:
        #     text_of_form = '📍'

    except Exception as e:
        text_of_form = 'Ошибка при формировании анкеты, обратитесь в поддержку: @something'
        logger.error('Ошибка при сборке анкеты: %s', e)
    finally:
        return text_of_form
