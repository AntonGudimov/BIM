from User import User
from password_strength import PasswordStats
from KeyboardStatistic import KeyboardStatistic


class KeyboardLogic:
    def __init__(self):
        self.__user = User()
        self.__keyboard_statistic = KeyboardStatistic()

    @property
    def user(self):
        return self.__user

    @property
    def keyboard_statistic(self):
        return self.__keyboard_statistic

    @user.setter
    def user(self, user):
        self.__user = user

    @keyboard_statistic.setter
    def keyboard_statistic(self, keyboard_and_statistic):
        self.__keyboard_statistic = keyboard_and_statistic

    def add_speed(self, daytime):
        self.__keyboard_statistic.add_speed(daytime, self.__user.password)

    def add_pressed_key(self, pressed_key):
        self.__keyboard_statistic.add_pressed_key(pressed_key)

    def add_pressed_time(self, pressed_time):
        self.__keyboard_statistic.add_pressed_time(pressed_time)

    # Расчет сложности парольной фразы
    def examine_password_for_complexity(self):
        stats = PasswordStats(self.__user.password)
        complexity = stats.strength()

        if 0 <= complexity < 0.33:
            return "password is weak"
        elif 0.33 <= complexity < 0.66:
            return "password is medium"
        elif 0.66 <= complexity < 1:
            return "password is strong"

    def calculate_input_dynamic(self):
        chair_pairs = self.get_char_pairs_from_password()
        time_pairs = self.keyboard_statistic.calculate_input_dynamic(self.__user.password)
        return chair_pairs, time_pairs

    def calculate_mean_speed(self):
        return self.__keyboard_statistic.calculate_mean_speed()

    def calculate_var_speed(self):
        return self.__keyboard_statistic.calculate_var_speed()

    def calculate_speed(self, start_time, end_time):
        speed = len(self.__user.password) / (end_time - start_time)
        return speed

    def get_char_pairs_from_password(self):
        return [self.__user.password[i] + "-" + self.__user.password[i + 1]
                for i in range(len(self.__user.password) - 1)]

    def init_pressed_released_key_times_dict(self):
        self.__keyboard_statistic.init_pressed_released_key_times_dict(self.__user.password)

    def add_pressed_released_key_time_el(self, char, pressed_or_released_time):
        if not self.__keyboard_statistic.pressed_released_key_times:
            self.init_pressed_released_key_times_dict()
        self.__keyboard_statistic.add_pressed_released_key_time_el(char, pressed_or_released_time)

    def calculate_key_hold(self):
        return self.__keyboard_statistic.calculate_key_hold()

    def pressed_keys_clear(self):
        self.__keyboard_statistic.pressed_keys_clear()

    def pressed_times_clear(self):
        self.__keyboard_statistic.pressed_times_clear()

    def pressed_released_key_times_dict_clear(self):
        self.__keyboard_statistic.pressed_released_key_times_dict_clear()

    # Функции для 2 лабы
    def add_value_to_func_t(self):
        self.__keyboard_statistic.add_value_to_func_t()

    def form_vector(self):
        return self.__keyboard_statistic.form_vector(len(self.__user.password))



