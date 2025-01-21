from aiogram import Router, types
from aiogram.filters import Command
from bot.keyboards.buttons import put_away_like_addition_markup
from bot.handlers.messages.start import start
from bot.logs.logger import logger
from database.database_code import Database

router = Router()

db = Database()


@router.message(Command("delete"))
async def delete_form_command(message: types.Message):
    try:
        db.delete_form(user_id=message.chat.id)
        await message.answer(text="Твоя анкета удалена!", reply_markup=put_away_like_addition_markup)
        await start(message=message)
    except Exception as e:
        logger.error("Возникла ошибка в delete_form_command: %s", e)