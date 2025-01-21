from yookassa import Configuration, Payment
from bot.services.payments.payments_config import yookassa_shop_id, yookassa_secret_key

Configuration.account_id = yookassa_shop_id
Configuration.secret_key = yookassa_secret_key


async def create_yoomoney_payment(user_id: int, message_to_delete_id: int):
    payment = Payment.create({
        "amount": {
            "value": "150",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/beloved_date_bot"
        },
        "description": "Покупка 👑Premium👑-подписки",
        "metadata": {
            "user_id": user_id,
            "message_id": message_to_delete_id
        }
    })
    return payment.confirmation.confirmation_url


