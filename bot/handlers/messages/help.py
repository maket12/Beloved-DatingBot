from aiogram import Router, types
from aiogram.filters import Command
from bot.logs.logger import logger

router = Router()


@router.message(Command('help'))
async def get_help_command(message: types.Message):
    try:
        await message.answer(text='Этот бот разработан Владимиром(@zervany)\n'
        'По всем вопросам по работоспособности бота обращаться ко мне.')
    except Exception as e:
        logger.error('Ошибка в help: %s', e)