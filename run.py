import asyncio
from bot.main import main
from bot.services.payments.yoomoney.successful_payment import app

if __name__ == "__main__":
    asyncio.run(main())
