from aiogram import Router, types
from bot.logs.logger import logger

router = Router()


@router.pre_checkout_query()
async def answer_pre_check_query(check_query: types.PreCheckoutQuery):
    try:
        await check_query.answer(ok=True)
    except Exception as e:
        logger.error("Возникла ошибка в answer_pre_check_query: %s", e)
