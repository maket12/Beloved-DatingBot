import asyncio
from aiogram import Router, types, F
from bot.bot_instance import bot
from bot.utils.like_form.notification_about_like import check_like
from bot.utils.send_form_utils.send_form import send_form
from bot.keyboards.buttons import start_scrolling_markup
from database.database_code import Database
from bot.logs.logger import logger


router = Router()

db = Database()


@router.callback_query(F.data.startswith("check_like"))
async def check_like_handler(call: types.CallbackQuery):
    try:
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await asyncio.sleep(1.5)

        like_id = int(call.data.split("_")[-1])
        await check_like(like_id=like_id)
    except Exception as e:
        logger.error("Возникла ошибка в check_like_handler: %s", e)


@router.callback_query(F.data == "skip_like")
async def skip_like(call: types.CallbackQuery):
    try:
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    except Exception as e:
        logger.error("Возникла ошибка в skip_like: %s", e)


@router.callback_query(F.data == "put_away_addition")
async def put_away_addition(call: types.CallbackQuery):
    try:
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    except Exception as e:
        logger.error("Возникла ошибка в put_away_addition: %s", e)


@router.callback_query(F.data.startswith("answer_like"))
async def answer_like(call: types.CallbackQuery):
    like_id = int(call.data.split('_')[-1])
    try:
        like_data = db.get_like_by_its_id(like_id=like_id)
        who_liked_form_id = like_data[2]
        who_liked_user_id = db.get_user_id_by_form_id(form_id=who_liked_form_id)

        # Получаем username у who_liked
        chat = await bot.get_chat(chat_id=who_liked_user_id)
        who_liked_username = chat.username

        # Отправляем каждому пользователю контакты для связи
        await bot.edit_message_text(text=f"Начать общаться👉 @{who_liked_username}",
                                    chat_id=call.from_user.id, message_id=call.message.message_id)

        await asyncio.sleep(3)

        await bot.send_message(chat_id=call.from_user.id, text="Можем продолжить поиск👇",
                               reply_markup=start_scrolling_markup)

        await asyncio.sleep(45)  # Пауза

        await send_form(user_id=who_liked_user_id, form_user_id=call.from_user.id, is_mutual_like=True)
        await bot.send_message(chat_id=who_liked_user_id,
                               text=f"Начать общаться👉 @{call.from_user.username}")
    except Exception as e:
        logger.error("Возникла ошибка в answer_like: %s", e)
    finally:
        db.delete_like(like_id=like_id)  # Удаляем лайк из БД


@router.callback_query(F.data.startswith("answer_dislike"))
async def answer_dislike(call: types.CallbackQuery):
    like_id = int(call.data.split('_')[-1])
    try:
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await asyncio.sleep(2)
        await bot.send_message(chat_id=call.from_user.id, text="Можем продолжить поиск👇",
                               reply_markup=start_scrolling_markup)
    except Exception as e:
        logger.error("Возникла ошибка в answer_dislike: %s", e)
    finally:
        db.delete_like(like_id=like_id)  # Удаляем лайк из БД

