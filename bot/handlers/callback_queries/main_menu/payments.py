from aiogram import Router, types, F
from bot.bot_instance import bot
from bot.services.payments.sberbank.sberbank_payment import send_sberbank_invoice
from bot.services.payments.yoomoney.yoomoney_invoice import send_yoomoney_invoice
from bot.logs.logger import logger


router = Router()


@router.callback_query(F.data.startswith("payment"))
async def choose_payment(call: types.CallbackQuery):
    try:
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

        payment_type = call.data.split("_")[1]

        if payment_type == "sberbank":
            await send_sberbank_invoice(user_id=call.from_user.id)
        elif payment_type == "yoomoney":
            await send_yoomoney_invoice(user_id=call.from_user.id, message_id=call.message.message_id+1)
    except Exception as e:
        logger.error("Возникла ошибка в choose_payment: %s", e)
