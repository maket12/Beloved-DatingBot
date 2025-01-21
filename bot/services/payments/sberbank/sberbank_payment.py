from bot.bot_instance import bot
from bot.services.payments.payments_config import *
from bot.logs.logger import logger


async def send_sberbank_invoice(user_id: int):
    try:
        await bot.send_invoice(chat_id=user_id, title=payment_title, description=payment_description,
                               payload=payment_payload, provider_token=sberbank_token,
                               currency=payment_currency,
                               photo_url="https://cdn-icons-png.flaticon.com/256/1657/1657088.png",
                               prices=payment_prices)
    except Exception as e:
        logger.error("Возникла ошибка в send_sberbank_invoice: %s", e)
