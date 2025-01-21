from aiogram import Router, types, F
from bot.bot_instance import bot
from bot.keyboards.buttons import profile_markup
from database.database_code import Database
from bot.logs.logger import logger


router = Router()

db = Database()


@router.callback_query(F.data == "profile")
async def profile(call: types.CallbackQuery):
    try:
        await bot.edit_message_text(text="Выбери необходимый параметр👇",
                                    chat_id=call.from_user.id,
                                    message_id=call.message.message_id,
                                    reply_markup=profile_markup
                                    )
    except Exception as e:
        logger.error("Возникла ошибка в profile: %s", e)


@router.callback_query(F.data == "likes")
async def likes(call: types.CallbackQuery):
    try:
        form_id = db.get_user_value(user_id=call.from_user.id, name="id")
        likes_amount = int(db.count_users_likes(users_form_id=form_id))

        if not likes_amount:
            await call.answer(text="На данный момент тебя никто не лайкнул", show_alert=True)
        else:
            pass
    except Exception as e:
        logger.error("Возникла ошибка в likes: %s", e)
