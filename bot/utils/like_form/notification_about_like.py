from bot.bot_instance import bot
from bot.keyboards.buttons import create_check_like_markup, create_like_answers_markup, put_away_like_addition_markup
from bot.utils.send_form_utils.send_form import send_form
from database.database_code import Database
from bot.logs.logger import logger


db = Database()


async def send_notification_about_like(user_id: int):
    try:
        form_id = db.get_user_value(user_id=user_id, name="id")
        like_id = db.get_last_like_id(form_id=form_id)

        await bot.send_message(chat_id=user_id, text="Кто-то лайкнул твою анкету🩷\n"
                                                     "Нажми кнопку ниже, чтобы посмотреть",
                               reply_markup=await create_check_like_markup(like_id=like_id))
    except Exception as e:
        logger.error("Возникла ошибка send_notification_about_like: %s", e)


# Приложение к лайку
async def check_like_addition(user_id: int, addition: tuple):  # Только доп параметры в кортеже
    try:
        if not any(addition_parameter for addition_parameter in addition):
            return

        if addition[0]:
            await bot.send_message(chat_id=user_id,
                                   text=f"Также для тебя есть сообщение:\n<tg-spoiler>{addition[0]}</tg-spoiler>",
                                   reply_markup=put_away_like_addition_markup, parse_mode="html")
        elif addition[1]:
            await bot.send_photo(chat_id=user_id, photo=addition[1],
                                 caption="Также для тебя есть фото:", has_spoiler=True)
        elif addition[2]:
            await bot.send_video(chat_id=user_id, video=addition[2],
                                 caption="Также для тебя есть видео:", has_spoiler=True)
        elif addition[3]:
            await bot.send_voice(chat_id=user_id, voice=addition[3],
                                 caption="Также для тебя есть голосовое сообщение:")

    except Exception as e:
        logger.error("Возникла ошибка в check_like_addition: %s", e)


# Извлекаем всё из БД и формируем сообщение
async def check_like(like_id: int):
    try:
        like_data = db.get_like_by_its_id(like_id=like_id)  # Данные о лайке
        logger.info(f"{like_data}")
        who_liked_user_id = db.get_user_id_by_form_id(form_id=like_data[2])
        liked_user_id = db.get_user_id_by_form_id(form_id=like_data[1])

        # Теперь отправляем анкету
        await send_form(user_id=liked_user_id, form_user_id=who_liked_user_id)

        # Также отправляем дополнение, если имеется
        addition_data = (like_data[4], like_data[5], like_data[6], like_data[7])
        await check_like_addition(user_id=liked_user_id, addition=addition_data)

        await bot.send_message(chat_id=liked_user_id, text="Выбери действие для анкеты:",
                               reply_markup=await create_like_answers_markup(like_id=like_data[0]))
    except Exception as e:
        logger.error("Вознилка ошибка в check_like: %s", e)
