from KeyboardLogic import KeyboardLogic
from User import User
import _sqlite3 as sql


class DataBase:
    def __init__(self, path):
        self.__conn = sql.connect(path)

    def register_user(self, user_statistic: KeyboardLogic, key_overlaying_list: tuple, mean_pressed_release_diff: dict,
                      vector_list: list):
        self.insert_user(user_statistic.user)
        user_id = self.select_user_id(user_statistic.user)
        self.insert_complexity(user_statistic.examine_password_for_complexity(), user_id)
        self.insert_input_password_speed(user_statistic.keyboard_statistic.speed_dict,
                                         user_statistic.calculate_mean_speed(),
                                         user_statistic.calculate_var_speed(), user_id)
        self.insert_input_password_dynamic(user_statistic.calculate_input_dynamic(), user_id)
        self.insert_key_overlaying(key_overlaying_list, user_id)
        self.insert_key_hold(mean_pressed_release_diff, user_id)
        self.insert_vector(vector_list, user_id)

    def insert_user(self, user: User):
        # don't forget to implement try-catch
        sql_query = 'INSERT INTO USER (login, password) values (?, ?)'
        data_vector = [(user.login, user.password)]
        with self.__conn:
            self.__conn.executemany(sql_query, data_vector)

    def select_user_id(self, user: User):
        user_id = -1
        cur = self.__conn.cursor()
        with self.__conn:
            cur.execute("SELECT * FROM USER WHERE login=?", (user.login,))
            rows = cur.fetchall()
            user_id = rows[0][0]
        return user_id

    def insert_complexity(self, complexity, user_id):
        sql_query = 'INSERT INTO PASSWORD_COMPLEXITY (complexity, user_id) values (?, ?)'
        data_vector = [
            (complexity,
             user_id)
        ]
        with self.__conn:
            self.__conn.executemany(sql_query, data_vector)

    def insert_input_password_speed(self, input_password_speed, mean_speed, var_speed, user_id):
        for items in input_password_speed.items():
            day_time = items[0]
            if len(items[1]):
                for input_password_speed in items[1]:
                    sql_query = 'INSERT INTO INPUT_PASSWORD_SPEED (speed, day_time, user_id) values (?, ?, ?)'
                    data_vector = [
                        (input_password_speed,
                         day_time,
                         user_id)
                    ]
                    with self.__conn:
                        self.__conn.executemany(sql_query, data_vector)

                sql_query = 'INSERT INTO MEAN_SPEED (value, day_time, user_id) values (?, ?, ?)'
                data_vector = [
                    (mean_speed[day_time],
                     day_time,
                     user_id)
                ]
                with self.__conn:
                    self.__conn.executemany(sql_query, data_vector)

                sql_query = 'INSERT INTO VAR_SPEED (value, day_time, user_id) values (?, ?, ?)'
                data_vector = [
                    (var_speed[day_time],
                     day_time,
                     user_id)
                ]
                with self.__conn:
                    self.__conn.executemany(sql_query, data_vector)

    def insert_input_password_dynamic(self, time_pairs, user_id):
        for time_pair in time_pairs[1]:
            sql_query = 'INSERT INTO INPUT_PASSWORD_DYNAMIC (value, user_id) values (?, ?)'
            data_vector = [
                (time_pair,
                 user_id)
            ]
            with self.__conn:
                self.__conn.executemany(sql_query, data_vector)

    def insert_key_overlaying(self, key_overlaying_list, user_id):
        for i in range(len(key_overlaying_list)):
            if key_overlaying_list[i]:
                for j in range(key_overlaying_list[i]):
                    sql_query = 'INSERT INTO KEY_OVERLAYING (type, user_id) values (?, ?)'
                    data_vector = [
                        (i + 1,     # i + 1 - type of overlaying
                         user_id)
                    ]
                    with self.__conn:
                        self.__conn.executemany(sql_query, data_vector)

    def insert_key_hold(self, key_hold_dict: dict, user_id):
        for key_hold_dict_pair in key_hold_dict.items():
            sql_query = 'INSERT INTO KEY_HOLD (key, time, user_id) values (?, ?, ?)'
            data_vector = [
                (key_hold_dict_pair[0],
                 key_hold_dict_pair[1],
                 user_id)
            ]
            with self.__conn:
                self.__conn.executemany(sql_query, data_vector)

    def insert_vector(self, vector, user_id):
        for item in vector:
            sql_query = 'INSERT INTO VECTOR_ELEMENT (value , user_id) values (?, ?)'
            data_vector = [
                (item,
                 user_id)
            ]
            with self.__conn:
                self.__conn.executemany(sql_query, data_vector)
