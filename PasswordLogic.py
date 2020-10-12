from password_strength import PasswordPolicy, PasswordStats


class PasswordLogic:
    def __init__(self):
        self.__username = ""
        self.__password = ""
        self.__speed_dict = {"morning": list(), "afternoon": list(), "evening": list(), "night": list()}
        self.__mean_speed_dict = {"morning": 0, "afternoon": 0, "evening": 0, "night": 0}
        self.__var_speed_dict = {"morning": 0, "afternoon": 0, "evening": 0, "night": 0}
        self.__pressed_keys = list()
        self.__pressed_times = list()
        self.__time_pairs = list()

    @property
    def user_name(self):
        return self.__username

    @property
    def password(self):
        return self.__password

    @property
    def speed_dict(self):
        return self.__speed_dict

    @property
    def mean_speed_dict(self):
        return self.__mean_speed_dict

    @property
    def var_speed_dict(self):
        return self.__var_speed_dict

    @property
    def pressed_keys(self):
        return self.__pressed_keys

    @property
    def pressed_times(self):
        return self.__pressed_times

    @property
    def time_pairs(self):
        return self.__time_pairs

    @user_name.setter
    def user_name(self, user_name):
        self.__username = user_name

    @password.setter
    def password(self, password):
        self.__password = password

    def add_speed(self, key, speed):
        self.__speed_dict[key].append(speed)

    def add_mean_speed(self, key, mean_speed):
        self.__mean_speed_dict[key] = mean_speed

    def add_var_speed(self, key, var_speed):
        self.__var_speed_dict[key] = var_speed

    def add_pressed_key(self, pressed_key):
        self.__pressed_keys.append(pressed_key)

    def add_pressed_time(self, pressed_time):
        self.__pressed_times.append(pressed_time)

    def clear_pressed_keys(self):
        self.__pressed_keys.clear()

    def clear_pressed_times(self):
        self.__pressed_times.clear()

    def examine_password_for_complexity(self):
        stats = PasswordStats(self.__password)
        complexity = stats.strength()

        if 0 <= complexity < 0.33:
            return "password is weak"
        elif 0.33 <= complexity < 0.66:
            return "password is medium"
        elif 0.66 <= complexity < 1:
            return "password is strong"

    def calculate_speed(self):
        speed = len(self.__password) / (self.__pressed_times[-1] - self.__pressed_times[0])
        return speed

    def calculate_input_dynamic(self):
        self.__time_pairs.clear()
        for i in range(len(self.__password) - 1, -1, -1):
            for j in range(len(self.__pressed_keys) - 1, -1, -1):
                if self.__password[i] == self.__pressed_keys[j]:
                    for k in range(j - 1, -1, -1):
                        if self.__password[i - 1] == self.__pressed_keys[k]:
                            self.__time_pairs.append(self.__pressed_times[j] - self.__pressed_times[k])
                            break
                    break

    def get_char_pairs_from_password(self):
        arr = list()
        for i in range(len(self.__password) - 1):
            arr.append(self.__password[i] + self.__password[i + 1])
        return arr


