import sqlite3

class BotDB:

    def __init__(self, db_file):
          #Соединяемся с базой
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
          #Проверяем, есть ли юзер в базе
          self.cursor.execute("""CREATE TABLE IF NOT EXISTS people(
                     id INTEGER PRIMARY KEY,
                     user_id INTEGER,
                     photo BLOB,
                     name TEXT,
                     description TEXT,
                     username TEXT,
                     course, INTEGER,
                     institute TEXT,
                     interests TEXT);
                  """)
          self.conn.commit()
          user_id = str(user_id).split(" ")
          user_id = ''.join(user_id)
          print(type(user_id), type('123'))
          result = self.cursor.execute("SELECT `id` FROM `people` WHERE `user_id` = ?", (user_id,))
          return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
          #Достаем id юзера в базе по его user_id
        result = self.cursor.execute("SELECT `id` FROM `people` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def update_description(self, description, user_id):
        self.cursor.execute("UPDATE people SET 'description' = ? WHERE 'user_id' = ?", (str(description), user_id,))
        self.conn.commit()

    def change_photo(self, photo, user_id):
        self.cursor.execute("UPDATE people SET 'photo' = ? WHERE 'user_id' = ?", (photo, user_id,))
        self.conn.commit()

    def add_user(self, user_id):
          #Добавляем юзера в базу
        self.cursor.execute("INSERT INTO `people` (`user_id`) VALUES (?)", (user_id,))
        return self.conn.commit()

    def add_name(self, name):
          #Добавляем name юзера
        self.cursor.execute("INSERT INTO `people` (`name`) VALUES (?)", (name,))
        return self.conn.commit()

    def add_description(self, description):
          #Добавляем description юзера
        self.cursor.execute("INSERT INTO `people` (`description`) VALUES (?)", (description,))
        return self.conn.commit()

    def add_institute(self, institute):
          #Добавляем institute юзера
        self.cursor.execute("INSERT INTO `people` (`institute`) VALUES (?)", (institute,))
        return self.conn.commit()

    def add_interests(self, interests):
          #Добавляем interests юзера
        self.cursor.execute("INSERT INTO `people` (`interests`) VALUES (?)", (interests,))
        return self.conn.commit()

    def create_user(self, user_id, photo, name, description, username, course, institute, interests):
        self.cursor.execute("INSERT INTO 'people' (user_id, photo, name, description, username, course, institute, interests) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (user_id, None, name, description, username, int(course), institute, interests,))

    def select_all_hobby(self, user_id):
        res = self.cursor.execute("SELECT user_id, interests FROM people WHERE user_id != ?", (user_id,))
        return list(res)

    def get_user(self, user_id):
        res = self.cursor.execute("SELECT photo, name, description, interests, username FROM people WHERE user_id = ?", (user_id,))
        return list(res)

    def get_intrrest(self, user_id):
        res = self.cursor.execute("SELECT interests FROM people WHERE user_id = ?",
                                  (user_id,))
        return list(res)

    def update_photo(self, photo, user_id):
        self.cursor.execute("UPDATE people SET 'photo' = ? WHERE 'user_id' = ?", (photo, user_id,))
        self.conn.commit()

    def close(self):
          #Закрываем базу
        self.conn.close()