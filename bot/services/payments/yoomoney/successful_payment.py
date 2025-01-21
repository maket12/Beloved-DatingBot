from flask import Flask, request, jsonify
from bot.services.payments.successful_payment import successful_payment_handler
from bot.logs.logger import logger


app = Flask(__name__)


@app.route("/payment_yoomoney", methods=["POST"])
async def payment_notification():
    try:
        data = request.json["object"]
        logger.info(f"Получили объект платежа: {data}")
        if data["status"] == "succeeded":
            user_id = data["metadata"]["user_id"]
            message_id = data["metadata"]["message_id"]
            await successful_payment_handler(user_id=user_id, message_id=message_id)
        return jsonify({"status": "ok"})
    except Exception as e:
        logger.error("Возникла ошибка в payment_notification: %s", e)

@app.route("/hey")
async def hey():
    return "Hello, World!"


