import asyncio
from aiogram import Router, types, F
from bot.bot_instance import bot
from bot.handlers.messages.main_menu import main_menu
from bot.keyboards.buttons import payments_markup
from database.database_code import Database
from bot.logs.logger import logger


router = Router()

db = Database()


@router.callback_query(F.data == "change_scrolling_parameters")
async def change_scrolling_parameters(call: types.CallbackQuery):
    try:
        await call.answer(text="Данная функция сейчас недоступна!", show_alert=True)
    except Exception as e:
        logger.error("Возникла ошибка в change_scrolling_parameters: %s", e)


@router.callback_query(F.data == "buy_premium")
async def buy_premium(call: types.CallbackQuery):
    try:
        check_premium = db.get_user_value(user_id=call.from_user.id, name="is_premium")
        if not check_premium:
            await bot.send_message(chat_id=call.from_user.id,
                                   text="Выбери вариант оплаты из предложенных:",
                                   message_effect_id="5104841245755180586",
                                   reply_markup=payments_markup)
        else:
            await call.answer(text="У тебя уже куплен Premium", show_alert=True)
    except Exception as e:
        logger.error("Возникла ошибка в buy_premium: %s", e)


@router.callback_query(F.data == "menu_back")
async def menu_back(call: types.CallbackQuery):
    try:
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await asyncio.sleep(1)
        await main_menu(message=call)
    except Exception as e:
        logger.error("Возникла ошибка в buy_premium: %s", e)
