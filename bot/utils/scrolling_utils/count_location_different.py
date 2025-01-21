from bot.logs.logger import logger
from geopy.distance import distance


async def count_geo_different(first_location: tuple, second_location: tuple, exactness=True):
    # Параметр exactness = True - для сортировки анкет, False - для пользовательского интерфейса
    try:
        dist = distance(first_location, second_location).meters
        if exactness:
            return round(dist, 2) if dist <= 50000 else None

        dist_rounded = round(dist)
        if dist_rounded < 100:
            dist_rounded = round(round(dist), -1)  # 47.55 --> 50
        elif 100 <= dist_rounded <= 50000:
            dist_rounded = round(round(dist), -2)  # 1150 --> 1200
        else:
            dist_rounded = None
        return dist_rounded
    except Exception as e:
        logger.error('Ошибка в count_geo_different:%s', e)
