from bot.utils.scrolling_utils.forms_queue import do_forms_queue
from bot.logs.logger import logger
import asyncio
from database.database_code import Database


db = Database()


# Функция обновления анкет(списков forms_row в БД)
async def update_all_forms(forms):  # Список ID
    try:
        logger.debug('Начинаем обновление анкет')
        for form in forms:
            logger.info(f'Выполняется обновление анкеты {form}...')
            await do_forms_queue(form)
        logger.debug('Обновление анкет завершено успешно!')
    except Exception as e:
        logger.error('Произошла ошибка при обновлении анкет: %s', e)


# Асинхронная функция для периодического выполнения update_all_forms
async def periodic_update():
    while True:
        forms_data = db.get_all_forms()
        forms_user_ids = [user_id[1] for user_id in forms_data]
        await update_all_forms(forms_user_ids)
        await asyncio.sleep(900)  # Пауза около 15 минут
