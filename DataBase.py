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

    def identify_user(self, password, vector: list):
        user_in_db = self.isUserOk(password)
        user_id = -1
        user_name = ""
        possibility_dict = dict()
        for i in range(len(user_in_db)):
            cur = self.__conn.cursor()
            with self.__conn:
                cur.execute("SELECT value FROM VECTOR_ELEMENT WHERE user_id=?", (user_in_db[i][0],))
                rows = cur.fetchall()
            possibility_dict[(user_in_db[i][0], user_in_db[i][1])] = 0
            mean_and_var_vector = MathLogic.calculate_mean_and_var_vector_values(rows, len(vector))
            for j in range(len(vector)):
                diff = pow(abs(mean_and_var_vector[0][j]) - abs(vector[j]), 2)
                #possibility_dict[(user_in_db[i][0], user_in_db[i][1])].append(diff)
                if diff <= mean_and_var_vector[1][j]:
                    possibility_dict[(user_in_db[i][0], user_in_db[i][1])] += 1 / len(vector)
                    #del possibility_dict[(user_in_db[i][0], user_in_db[i][1])]
                    #break
        #if len(possibility_dict):
            #mean_dict = MathLogic.calculate_mean_value(possibility_dict)
            #keys = list(mean_dict.keys())
            #vals = list(mean_dict.values())
            #min_val = min(vals)
            #user_id = keys[vals.index(min_val)][0]
            #user_name = keys[vals.index(min_val)][1]

        if len(possibility_dict):
            keys = list(possibility_dict.keys())
            values = list(possibility_dict.values())
            max_val = max(values)
            if max_val > 0.63:
                user_id = keys[values.index(max_val)][0]
                user_name = keys[values.index(max_val)][1]
        return user_id, user_name

    def verify_user(self, password, vector: list, id: int):
        user_in_db = self.isUserOk(password, id)
        if len(user_in_db):
            if user_in_db[0][0] == -1:
                return False, "Wrong input data"
            else:
                if user_in_db[0][1]:
                    cur = self.__conn.cursor()
                    with self.__conn:
                        cur.execute("SELECT value FROM VECTOR_ELEMENT WHERE user_id=?", (user_in_db[0][0],))
                        rows = cur.fetchall()
                        mean_and_var_vector = MathLogic.calculate_mean_and_var_vector_values(rows, len(vector))
                        posibility = 0
                        for i in range(len(vector)):
                            if pow(abs(mean_and_var_vector[0][i]) - abs(vector[i]), 2) <= mean_and_var_vector[1][i]:
                                posibility += 1 / len(vector)
                        if posibility > 0.6:
                            return True, user_in_db[0][1]
                        else:
                            return False, "Wrong input data"
                else:
                    return False, "Wrong input data"
        return False, "Wrong input data"

    def isUserOk(self, password, input_user_id=-1):
        user_id = -1
        if input_user_id != -1:
            cur = self.__conn.cursor()
            with self.__conn:
                cur.execute("SELECT * FROM USER WHERE id=? AND password=?", (input_user_id, password,))
                rows = cur.fetchall()
        else:
            cur = self.__conn.cursor()
            with self.__conn:
                cur.execute("SELECT * FROM USER WHERE password=?", (password,))
                rows = cur.fetchall()
        return rows

    def select_users(self):
        cur = self.__conn.cursor()
        with self.__conn:
            cur.execute("SELECT * FROM USER")
            rows = cur.fetchall()
        return rows

    def select_password_complexity(self):
        cur = self.__conn.cursor()
        with self.__conn:
            cur.execute("SELECT * FROM PASSWORD_COMPLEXITY")
            rows = cur.fetchall()
        return rows

    def select_speed(self):
        cur = self.__conn.cursor()
        with self.__conn:
            cur.execute("SELECT * FROM INPUT_PASSWORD_SPEED")
            rows = cur.fetchall()
        return rows

    def select_input_password_dynamic(self):
        cur = self.__conn.cursor()
        with self.__conn:
            cur.execute("SELECT * FROM INPUT_PASSWORD_DYNAMIC")
            rows = cur.fetchall()
        return rows

    def select_key_overlaying(self):
        cur = self.__conn.cursor()
        with self.__conn:
            cur.execute("SELECT * FROM KEY_OVERLAYING")
            rows = cur.fetchall()
        return rows

    def select_key_hold(self):
        cur = self.__conn.cursor()
        with self.__conn:
            cur.execute("SELECT * FROM KEY_HOLD")
            rows = cur.fetchall()
        return rows

    def select_vector(self):
        cur = self.__conn.cursor()
        with self.__conn:
            cur.execute("SELECT * FROM VECTOR_ELEMENT")
            rows = cur.fetchall()
        return rows

    def add_user(self, new_login, new_password):
        sql = 'INSERT INTO USER (login, password) values (?, ?)'
        cur = self.__conn.cursor()
        cur.execute(sql, [new_login, new_password])
        self.__conn.commit()

    def add_password_complexity(self, new_complexity, new_user_id):
        sql = 'INSERT INTO PASSWORD_COMPlEXITY (complexity, user_id) values (?, ?)'
        cur = self.__conn.cursor()
        cur.execute(sql, [new_complexity, new_user_id])
        self.__conn.commit()

    def add_input_password_speed(self, new_speed, new_day_time, new_user_id):
        sql = 'INSERT INTO INPUT_PASSWORD_SPEED (speed, day_time, user_id) values (?, ?, ?)'
        cur = self.__conn.cursor()
        cur.execute(sql, [new_speed, new_day_time, new_user_id])
        self.__conn.commit()

    def add_input_password_dynamic(self, new_value, new_user_id):
        sql = 'INSERT INTO INPUT_PASSWORD_DYNAMIC (value, user_id) values (?, ?)'
        cur = self.__conn.cursor()
        cur.execute(sql, [new_value, new_user_id])
        self.__conn.commit()

    def add_input_key_overlaying(self, new_type, new_user_id):
        sql = 'INSERT INTO KEY_HOLD (type, user_id) values (?, ?)'
        cur = self.__conn.cursor()
        cur.execute(sql, [new_type, new_user_id])
        self.__conn.commit()

    def add_input_key_hold(self, new_key, new_time, new_user_id):
        sql = 'INSERT INTO KEY_HOLD (key, time, user_id) values (?, ?, ?)'
        cur = self.__conn.cursor()
        cur.execute(sql, [new_key, new_time, new_user_id])
        self.__conn.commit()

    def add_vector(self, new_value, new_user_id):
        sql = 'INSERT INTO VECTOR_ELEMENT (value, user_id) values (?, ?)'
        cur = self.__conn.cursor()
        cur.execute(sql, [new_value, new_user_id])
        self.__conn.commit()



    def edit_user(self, id, new_login, new_password):
        sql = 'UPDATE USER SET login=?, password=? WHERE id=?'
        cur = self.__conn.cursor()
        cur.execute(sql, [new_login, new_password, id])
        self.__conn.commit()

    def edit_password_complexity(self, id, new_complexity, new_user_id):
        sql = 'UPDATE PASSWORD_COMPlEXITY SET complexity=?, user_id=? WHERE id=?'
        cur = self.__conn.cursor()
        cur.execute(sql, [new_complexity, new_user_id, id])
        self.__conn.commit()

    def edit_input_password_speed(self, id, new_speed, new_day_time, new_user_id):
        sql = 'UPDATE INPUT_PASSWORD_SPEED SET speed=?, day_time=?, user_id=? WHERE id=?'
        cur = self.__conn.cursor()
        cur.execute(sql, [new_speed, new_day_time, new_user_id, id])
        self.__conn.commit()

    def edit_input_password_dynamic(self, id, new_value, new_user_id):
        sql = 'UPDATE INPUT_PASSWORD_DYNAMIC SET value =?, user_id=? WHERE id=?'
        cur = self.__conn.cursor()
        cur.execute(sql, [new_value, new_user_id, id])
        self.__conn.commit()

    def edit_input_key_overlaying(self, id, new_type, new_user_id):
        sql = 'UPDATE KEY_HOLD SET type =?, user_id=? WHERE id=?'
        cur = self.__conn.cursor()
        cur.execute(sql, [new_type, new_user_id, id])
        self.__conn.commit()

    def edit_input_key_hold(self, id, new_key, new_time, new_user_id):
        sql = 'UPDATE KEY_HOLD SET key =?, time=?, user_id=? WHERE id=?'
        cur = self.__conn.cursor()
        cur.execute(sql, [new_key, new_time, new_user_id, id])
        self.__conn.commit()

    def edit_vector(self, id, new_value, new_user_id):
        sql = 'UPDATE VECTOR_ELEMENT SET value =?, user_id=? WHERE id=?'
        cur = self.__conn.cursor()
        cur.execute(sql, [new_value, new_user_id, id])
        self.__conn.commit()

    def delete_user(self, id):
        sql = 'DELETE FROM USER WHERE id=?'
        cur = self.__conn.cursor()
        cur.execute(sql, [id])
        self.__conn.commit()

    def delete_password_compexity(self, id):
        sql = 'DELETE FROM PASSWORD_COMPLEXITY WHERE id=?'
        cur = self.__conn.cursor()
        cur.execute(sql, [id])
        self.__conn.commit()

    def delete_input_password_speed(self, id):
        sql = 'DELETE FROM INPUT_PASSWORD_SPEED WHERE id=?'
        cur = self.__conn.cursor()
        cur.execute(sql, [id])
        self.__conn.commit()

    def delete_input_password_dynamic(self, id):
        sql = 'DELETE FROM INPUT_PASSWORD_DYNAMIC WHERE id=?'
        cur = self.__conn.cursor()
        cur.execute(sql, [id])
        self.__conn.commit()

    def delete_key_overlaying(self, id):
        sql = 'DELETE FROM KEY_OVERLAYING WHERE id=?'
        cur = self.__conn.cursor()
        cur.execute(sql, [id])
        self.__conn.commit()

    def delete_key_hold(self, id):
        sql = 'DELETE FROM KEY_HOLD WHERE id=?'
        cur = self.__conn.cursor()
        cur.execute(sql, [id])
        self.__conn.commit()

    def delete_vector_element(self, id):
        sql = 'DELETE FROM VECTOR_ELEMENT WHERE id=?'
        cur = self.__conn.cursor()
        cur.execute(sql, [id])
        self.__conn.commit()

