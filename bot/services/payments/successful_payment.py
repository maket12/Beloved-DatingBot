import asyncio
from bot.bot_instance import bot
from bot.keyboards.buttons import to_menu_markup
from database.database_code import Database
from bot.logs.logger import logger

db = Database()


async def successful_payment_handler(user_id: int, message_id: int):
    try:
        db.add_premium_user(user_id=user_id)  # Добавляем Premium юзера

        db.set_user_value(user_id=user_id, is_premium=1)  # Вносим в основную таблицу users

        await bot.delete_message(chat_id=user_id, message_id=message_id)
        await asyncio.sleep(1)
        await bot.send_animation(chat_id=user_id,
                                 animation="https://i.pinimg.com/originals/ee/a9/4b/eea94b0c0a3be17d2973ac2a44531458.gif",
                                 message_effect_id="5159385139981059251")
        await bot.send_message(chat_id=user_id, text="Спасибо за покупку💜💜\n"
                                "Тебе выдан Premium статус на месяц, скорее же опробуй новые функции!",
                               reply_markup=to_menu_markup)
    except Exception as e:
        logger.error("Возникла ошибка в successful_payment_handler: %s", e)
