import logging
import colorlog
import os

# Определение абсолютного пути к файлу журнала
LOG_FILE = os.path.join(os.path.dirname(__file__), 'logs', 'project.log')

# Форматтер для цветного консольного вывода
color_formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
)

# Создание обработчика файла
file_handler = logging.FileHandler('bot/logs/project.log')
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s [line:%(lineno)d]')
file_handler.setFormatter(file_formatter)

# Настройка логгера
logger = colorlog.getLogger()
logger.setLevel(logging.DEBUG)

# Добавление цветного обработчика и обработчика файла
console_handler = logging.StreamHandler()
console_handler.setFormatter(color_formatter)
logger.addHandler(console_handler)
logger.addHandler(file_handler)

logging.getLogger("asyncio").setLevel(logging.ERROR)
logging.getLogger("aiogram").setLevel(logging.ERROR)
logging.getLogger("sqlite3").setLevel(logging.ERROR)
logging.getLogger("flask").setLevel(logging.ERROR)
