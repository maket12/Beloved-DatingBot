from bot.bot_instance import bot
from bot.services.payments.yoomoney.yoomoney_payment import create_yoomoney_payment
from bot.keyboards.buttons import create_payment_button
from bot.logs.logger import logger


async def send_yoomoney_invoice(user_id: int, message_id: int):
    try:
        pay_url = await create_yoomoney_payment(user_id=user_id,
                                                message_to_delete_id=message_id)  # Получаем ссылку на оплату
        await bot.send_message(chat_id=user_id, text="Нажми, чтобы оплатить👇",
                               reply_markup=await create_payment_button(url=pay_url))
    except Exception as e:
        logger.error("Возникла ошибка в send_yoomoney_invoice: %s", e)
