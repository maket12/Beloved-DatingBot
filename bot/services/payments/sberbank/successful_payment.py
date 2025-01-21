from aiogram import Router, types, F
from bot.services.payments.successful_payment import successful_payment_handler
from database.database_code import Database
from bot.logs.logger import logger


router = Router()

db = Database()


@router.message(F.successful_payment)
async def sberbank_successful_payment(payment: types.Message):
    try:
        await successful_payment_handler(user_id=payment.from_user.id,
                                         message_id=payment.message_id)
    except Exception as e:
        logger.error("Возникла ошибка в sberbank_successful_payment: %s", e)
