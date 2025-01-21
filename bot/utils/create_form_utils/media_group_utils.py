from aiogram.utils.media_group import MediaGroupBuilder
from bot.utils.create_form_utils.form_text_utils import create_form_txt
from bot.logs.logger import logger
from database.database_code import Database
from bot.bot_instance import bot


db = Database()


# Функция создания медиа для анкеты
async def create_media_group(user_id: int, other_form_flag: bool, is_mutual_like: bool):

    media_to_send = MediaGroupBuilder()
    try:
        # Получаем все медиа и отправляем их в объект типа MediaGroup
        current_medias = db.get_user_value(user_id, 'profile_media').split('|')

        if len(current_medias) == 1:
            return 'single media', current_medias[0]
        else:
            form_text = await create_form_txt(user_id=user_id, other_form_flag=other_form_flag,
                                              is_mutual_like=is_mutual_like)

            media_to_send = MediaGroupBuilder(caption=form_text)

            for media_element in current_medias:
                if media_element:
                    file_info = await bot.get_file(media_element)
                    file_type = file_info.file_path.split('/')[0]  # Получаем данные о медиа
                    if file_type == 'photos':
                        media_to_send.add_photo(media=media_element)
                    else:
                        media_to_send.add_video(media=media_element)
        return media_to_send

    except Exception as e:
        logger.error('Ошибка при сборке анкеты: %s', e)

        media_to_send.add_photo(media=
                                "https://habrastorage.org/webt/ay/dp/mt/aydpmtdaqx8ueuo3kitujhva7mm.gif")
        return media_to_send


# Если предыдущая функция вернула 'single media'
async def create_form_with_single_media(user_id: int, media_file_id: str, other_form_flag=True,
                                        is_mutual_like=False):
    try:
        form_text = await create_form_txt(user_id, other_form_flag=other_form_flag,
                                          is_mutual_like=is_mutual_like)

        file_info = await bot.get_file(media_file_id)
        file_type = file_info.file_path.split('/')[0]

        if file_type == 'photos':
            return "photo", media_file_id, form_text
        else:
            return "video", media_file_id, form_text

    except Exception as e:
        logger.error('Ошибка при сборке анкеты: %s', e)
        return "photo", "https://habrastorage.org/webt/ay/dp/mt/aydpmtdaqx8ueuo3kitujhva7mm.gif", "Возникла ошибка! Обратитесь, пожалуйста, к администратору: @something"
