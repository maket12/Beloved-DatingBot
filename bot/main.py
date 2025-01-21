from aiogram import Dispatcher
import asyncio
from bot.main_router.include_routers import include_all_routers
from bot.logs.logger import logger
from bot.utils.update_form_utils.update_forms import periodic_update
from bot.bot_instance import bot
from database.database_code import Database


dp = Dispatcher()

db = Database()


# Функция для инициализации бота
async def init_bot():
    logger.debug('Бот был спроектирован и создан Владимиром (https://kwork.ru/user/maket14).')
    logger.warning(
        'Настоящее авторское право принадлежит только мне, копирование и присваивание любых фрагментов кода и проекта в целом без разрешения не допускается.')
    logger.debug('Подготовка к запуску')

    # Создание таблиц в базе данных
    db.create_tables()

    logger.debug('Запуск бота')
    logger.info('Бот запущен!')


# Основная функция запуска
async def main():
    await init_bot()

    include_all_routers(dp=dp)

    # Запуск функций бота и периодического обновления параллельно
    await asyncio.gather(
        dp.start_polling(bot),
        periodic_update()
    )


