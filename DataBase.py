from KeyboardLogic import KeyboardLogic
from User import User
from MathLogic import MathLogic
import _sqlite3 as sql


class DataBase:
    def __init__(self, path):
        self.__conn = sql.connect(path)

    def register_user(self, user_statistic: KeyboardLogic, key_overlaying_list: tuple,
                      chair_and_pairs,
                      mean_pressed_release_diff: dict,
                      vector_list: list):
        user_id = self.select_user_id(user_statistic.user)
        self.insert_input_password_speed(user_statistic.keyboard_statistic.speed_dict,
                                         user_statistic.calculate_mean_speed(),
                                         user_statistic.calculate_var_speed(), user_id)
        self.insert_input_password_dynamic(chair_and_pairs, user_id)
        self.insert_key_overlaying(key_overlaying_list, user_id)
        self.insert_key_hold(mean_pressed_release_diff, user_id)
        self.insert_vector(vector_list, user_id)

        return user_id

    def insert_user(self, user: User):
        # don't forget to implement try-catch
        sql_query = 'INSERT INTO USER (login, password) values (?, ?)'
        data_vector = [(user.login, user.password)]
        with self.__conn:
            self.__conn.executemany(sql_query, data_vector)
        return self.select_user_id(user)

    def select_user_id(self, user: User):
        user_id = -1
        cur = self.__conn.cursor()
        with self.__conn:
            cur.execute("SELECT * FROM USER WHERE login=?", (user.login,))
            rows = cur.fetchall()
            if rows:
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
                sql_query = 'INSERT INTO INPUT_PASSWORD_SPEED (speed, day_time, user_id) values (?, ?, ?)'
                data_vector = [
                    (items[1][-1],
                     day_time,
                     user_id)
                ]
                with self.__conn:
                    self.__conn.executemany(sql_query, data_vector)

    def insert_mean_and_var_speed(self, input_password_speed, mean_speed, var_speed, user_id):
        for items in input_password_speed.items():
            if items[1]:
                day_time = items[0]
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
                        (i + 1,  # i + 1 - type of overlaying
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

    def identify_user(self, user: User, vector: list):
        user_in_db = self.isUserOk(user)
        if user_in_db[0] == -1:
            return False, "Wrong input data"
        else:
            if user_in_db[1]:
                cur = self.__conn.cursor()
                with self.__conn:
                    cur.execute("SELECT value FROM VECTOR_ELEMENT WHERE user_id=?", (user_in_db[0],))
                    rows = cur.fetchall()
                    mean_and_var_vector = MathLogic.calculate_mean_and_var_vector_values(rows, len(vector))
                    for i in range(len(vector)):
                        if pow(abs(mean_and_var_vector[0][i]) - abs(vector[i]), 2) > mean_and_var_vector[1][i]:
                            return False, "Wrong input data"
                    return True, user_in_db[2], user_in_db[0]
            else:
                return False, "Wrong input data"

    def verify_user(self, user: User, vector: list, id: int):
        user_in_db = self.isUserOk(user, id)
        if user_in_db[0] == -1:
            return False, "Wrong input data"
        else:
            if user_in_db[1]:
                cur = self.__conn.cursor()
                with self.__conn:
                    cur.execute("SELECT value FROM VECTOR_ELEMENT WHERE user_id=?", (user_in_db[0],))
                    rows = cur.fetchall()
                    mean_and_var_vector = MathLogic.calculate_mean_and_var_vector_values(rows, len(vector))
                    for i in range(len(vector)):
                        if pow(abs(mean_and_var_vector[0][i]) - abs(vector[i]), 2) > mean_and_var_vector[1][i]:
                            return False, "Wrong input data"
                    return True, user_in_db[2]
            else:
                return False, "Wrong input data"

    def isUserOk(self, user: User, input_user_id=-1):
        user_id = -1
        if input_user_id != -1:
            cur = self.__conn.cursor()
            with self.__conn:
                cur.execute("SELECT * FROM USER WHERE id=? AND login=?", (input_user_id, user.login,))
                rows = cur.fetchall()
        else:
            cur = self.__conn.cursor()
            with self.__conn:
                cur.execute("SELECT * FROM USER WHERE login=?", (user.login,))
                rows = cur.fetchall()
        if rows:
            user_id = rows[0][0]
            if user.password == rows[0][2]:
                return user_id, True, user.login
        return user_id, False
