from bot.bot_instance import bot
from bot.utils.create_form_utils.media_group_utils import create_media_group, create_form_with_single_media
from bot.logs.logger import logger


async def send_form(user_id: int, form_user_id=None, other_form_flag=True, is_mutual_like=False):
    # user_id - кому отправляем анкету, u_id - какую анкету отправляем
    try:
        if other_form_flag:
            u_id = form_user_id
        else:
            u_id = user_id

        # Создаём объект типа MediaGroup
        media_to_send = await create_media_group(user_id=u_id, other_form_flag=other_form_flag,
                                                 is_mutual_like=is_mutual_like)

        if isinstance(media_to_send, tuple):
            form_data = await create_form_with_single_media(user_id=u_id, media_file_id=media_to_send[1],
                                                            other_form_flag=other_form_flag,
                                                            is_mutual_like=is_mutual_like)
            if form_data[0] == "photo":
                await bot.send_photo(chat_id=user_id, photo=form_data[1], caption=form_data[2])
            else:
                await bot.send_video(chat_id=user_id, video=form_data[1], caption=form_data[2])
        else:
            await bot.send_media_group(chat_id=user_id, media=media_to_send.build())
    except Exception as e:
        logger.error("Возникла ошибка в send_form: %s", e)
