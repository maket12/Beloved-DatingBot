from bot.logs.logger import logger
from database.database_code import Database
from bot.utils.scrolling_utils.count_location_different import count_geo_different


db = Database()


async def do_forms_queue(user_id):
    try:
        forms_queue = []  # Задаём список для анкет

        # Получаем пользовательские настройки
        users_data = db.get_users_form(user_id=user_id)
        users_city = users_data[9]
        users_age = users_data[3]
        users_goal = users_data[7]
        users_gender_choices = [users_data[4], users_data[5]]
        pre_users_location = users_data[10]

        if bool(pre_users_location):
            pre_users_location = pre_users_location.split('|')
            users_location = (pre_users_location[0], pre_users_location[1])
        else:
            users_location = None

        all_forms = db.get_all_forms()  # Получаем все анкеты
        for form in all_forms:
            if form[1] != user_id:  # Исключаем собственную анкету
                # Получаем параметры текущей анкеты
                forms_city, forms_age, forms_goal, forms_gender_choices, pre_forms_location = (form[9], form[3], form[7],
                                                                                               [form[4], form[5]],
                                                                                               form[10].split('|'))

                # Проверка на совпадение параметров анкеты
                if forms_city == users_city and (abs(forms_age-users_age) <= 5):
                    if users_gender_choices[0] in forms_gender_choices[1] and forms_gender_choices[0] in users_gender_choices[1]:
                        if users_location and bool(pre_forms_location[0]):
                            forms_location = (pre_forms_location[0], pre_forms_location[1])
                            dist = await count_geo_different(first_location=users_location,
                                                             second_location=forms_location)  # Высчитываем расстояние
                            forms_queue.append([form[0], dist])
                        else:
                            forms_queue.append([form[0], None])

        # Сортировка по расстоянию
        forms_queue.sort(key=lambda x: x[1] if x[1] else 0)
        # result_spic = []
        # while forms_queue:
        #     try:
        #         min_element = min(i[1] for i in forms_queue if i[1])
        #         k = -1  # Счётчик, чтобы получить индекс анкеты
        #
        #         for j in forms_queue:
        #             k += 1
        #             if j[1] == min_element:
        #                 break
        #
        #         result_spic.append(forms_queue[k])
        #
        #         forms_queue.remove(forms_queue[k])
        #     except ValueError:
        #         result_spic += forms_queue  # Добавляем анкеты без расстояния
        #         break

        db.set_user_value(user_id=user_id, forms_row=str(forms_queue))
        db.set_user_value(user_id=user_id, current_form_index=None)

        return forms_queue
    except Exception as e:
        logger.error('Ошибка в do_forms_queue: %s', e)

# print(do_forms_queue(5228009964))

