from aiogram import Router, types
from aiogram.filters import Command
from bot.bot_instance import bot
from bot.keyboards.buttons import main_menu_markup
from database.database_code import Database
from bot.logs.logger import logger


router = Router()

db = Database()


@router.message(Command("menu"))
async def main_menu(message: types.Message | types.CallbackQuery):
    try:
        form_id = db.get_user_value(user_id=message.from_user.id, name="id")
        likes_amount = int(db.count_users_likes(users_form_id=form_id))

        if not likes_amount:
            text = (f"Привет, {message.from_user.first_name}\n"
                    f"Тебя пока что никто не лайкнул")
        else:
            text = (f"Привет, {message.from_user.first_name}\n"
                    f"Сейчас тебя лайкнуло {likes_amount}👤")

        await bot.send_message(chat_id=message.from_user.id, text=text,
                               reply_markup=main_menu_markup)
    except Exception as e:
        logger.error("Возникла ошибка в main_menu: %s", e)
