from aiogram import Router, types
from aiogram.filters import Command
from bot.bot_instance import bot
from bot.keyboards.buttons import create_form_markup, form_settings_markup
from bot.utils.send_form_utils.send_form import send_form
from bot.logs.logger import logger
from database.database_code import Database


router = Router()


db = Database()


@router.message(Command('start'))
async def start(message: types.Message | types.CallbackQuery):
    try:
        if not db.user_exists(message.from_user.id):
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Привет💚! Я бот для знакомств Be_Loved\n'
                                        'У тебя ещё нет анкеты, давай же её создадим!',
                                   reply_markup=create_form_markup
                                   )
        else:
            await send_form(user_id=message.from_user.id, other_form_flag=False)  # Отправляем анкету

            await bot.send_message(chat_id=message.from_user.id, text='Всё верно?',
                                   reply_markup=form_settings_markup)
    except Exception as e:
        logger.error('Ошибка в старте: %s', e)
