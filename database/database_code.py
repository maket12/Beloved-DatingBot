import sqlite3
import os
import time

from bot.logs.logger import logger


class Database:
    def __init__(self, db_file="database.db"):

        # Получаем абсолютный путь к файлу базы данных относительно этого файла
        base_dir = os.path.dirname(os.path.abspath(__file__))
        absolute_path = os.path.join(base_dir, db_file)

        self.connection = sqlite3.connect(absolute_path)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        with self.connection:
            try:
                logger.debug('Подключение к базе данных')

                self.cursor.execute('CREATE TABLE IF NOT EXISTS "admins" ('
                                    '"id" INTEGER PRIMARY KEY AUTOINCREMENT,'
                                    '"user_id" INTEGER UNIQUE,'
                                    '"status" TEXT)')

                logger.info('База данных админов подключена успешно!')

                self.cursor.execute('CREATE TABLE IF NOT EXISTS "complaints" ('
                                    '"id" INTEGER PRIMARY KEY AUTOINCREMENT, '
                                    '"against_whom" INTEGER, '
                                    '"category" TEXT)')

                logger.info('База данных жалоб подключена успешно!')

                self.cursor.execute('CREATE TABLE IF NOT EXISTS "premium_users" ('
                                    '"id" INTEGER PRIMARY KEY AUTOINCREMENT,'
                                    '"user_id" INTEGER UNIQUE,'
                                    '"before_time" INTEGER)')

                logger.info('База данных Premium пользователей подключена успешно!')

                logger.debug('База данных подключена успешно')
            except Exception as e:
                logger.error(f'Ошибка при подключении к базе данных: {e}')

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM "users" WHERE "user_id" = ?', (user_id,)).fetchmany(1)
            return bool(len(result))

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute(f'INSERT INTO "users" ("user_id") VALUES (?)', (user_id,))

    def add_admin(self, user_id, position):
        with self.connection:
            return self.cursor.execute('INSERT INTO "admins" ("user_id", "position") VALUES (?, ?)', (user_id, position))

    def add_premium_user(self, user_id: int):
        with self.connection:
            before_time = int(time.time()) + (30 * 24 * 60 * 60)
                                            # ^^^^^^^^^^^^^^^^^^ Секунд в месяце
            return self.cursor.execute('INSERT INTO "premium_users" ("user_id", "before_time")'
                                       'VALUES (?, ?)', (user_id, before_time))

    def check_premium_users(self):
        current_time = int(time.time())  # Получаем текущее время
        with self.connection:
            premium_users = self.cursor.execute('SELECT * FROM "premium_users"').fetchall()
            users_spic = []
            for user in premium_users:
                if user[2] < current_time:
                    self.cursor.execute('DELETE FROM "premium_users" WHERE "id" = ?',
                                        (user[0]))  # Удаляем текущую запись из БД
                    users_spic.append(['expired', user[1]])
                if (user[2] - current_time) <= (60 * 60 * 24):
                    users_spic.append(['1 day', user[1]])
                if (user[2] - current_time) <= (60 * 60 * 24 * 7):
                    users_spic.append(['7 days', user[1]])

    def add_liked_form(self, form_id, who_liked_form_id, other_data):
        # Передаём other_data как кортеж, сначала название столбца, потом значение
        with self.connection:
            action_time = int(time.time())  # Определяем время события
            if not other_data:
                request = self.cursor.execute('INSERT INTO "liked_forms" ("form_id",'
                                              f'"who_liked_form_id", "action_time") VALUES (?, ?, ?)',
                                              (form_id, who_liked_form_id, action_time))
            else:
                request = self.cursor.execute(f'INSERT INTO "liked_forms" ("form_id", "who_liked_form_id",'
                                              f'"action_time", {other_data[0]}) VALUES (?, ?, ?, ?)',
                                              (form_id, who_liked_form_id,
                                               action_time, other_data[1]))
            return request

    def set_user_value(self, user_id, **kwargs):
        keys = kwargs.keys()
        columns = ', '.join([f'{key} = ?' for key in keys])

        values = list(kwargs.values())
        values.append(user_id)

        with self.connection:
            return self.cursor.execute(f'UPDATE "users" SET {columns} WHERE "user_id" = ?', values)

    def get_user_value(self, user_id, name):
        with self.connection:
            return self.cursor.execute(f'SELECT {name} FROM "users" WHERE "user_id" = ?', (user_id,)).fetchone()[0]

    def get_user_id_by_form_id(self, form_id):
        with self.connection:
            return self.cursor.execute('SELECT "user_id" FROM "users" WHERE "id" = ?', (form_id,)).fetchone()[0]

    def get_users_form(self, user_id):
        with self.connection:
            return self.cursor.execute('SELECT * FROM "users" WHERE "user_id" = ?', (user_id,)).fetchone()

    def get_all_forms(self):
        with self.connection:
            all_forms = self.cursor.execute('SELECT * FROM "users" WHERE "forms_row" IS NOT NULL').fetchall()  # Получаем все анкеты
            return all_forms

    def get_last_like_id(self, form_id: int):
        with self.connection:
            # Получаем всё о лайке с помощью параметра form_id
            return self.cursor.execute('SELECT "id" FROM "liked_forms" WHERE "form_id" = ?'
                                       'ORDER BY "form_id" DESC LIMIT 1',
                                       (form_id,)).fetchone()[0]

    def get_like_by_its_id(self, like_id: int):
        with self.connection:
            return self.cursor.execute('SELECT * FROM "liked_forms" WHERE "id" = ?',
                                       (like_id,)).fetchone()

    def count_users_likes(self, users_form_id: int):  # Сколько его лайкнули
        with self.connection:
            return self.cursor.execute('SELECT COUNT(*) FROM "liked_forms" WHERE "form_id" = ?',
                                       (users_form_id,)).fetchone()[0]

    def delete_form(self, user_id: int):
        with self.connection:
            return self.cursor.execute('DELETE FROM "users" WHERE "user_id" = ?',
                                       (user_id,))

    def delete_like(self, like_id: int):
        with self.connection:
            return self.cursor.execute('DELETE FROM "liked_forms" WHERE "id" = ?',
                                       (like_id,))
