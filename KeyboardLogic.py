from User import User
from password_strength import PasswordStats
from KeyboardStatistic import KeyboardStatistic


class KeyboardLogic:
    def __init__(self):
        self.__user = User()
        self.__keyboard_and_statistic = dict()

    @property
    def user(self):
        return self.__user

    @property
    def keyboard_and_statistic(self):
        return self.__keyboard_and_statistic

    @user.setter
    def user(self, user):
        self.__user = user

    @keyboard_and_statistic.setter
    def keyboard_and_statistic(self, keyboard_and_statistic):
        self.__keyboard_and_statistic = keyboard_and_statistic

    def add_keyboard(self, keyboard):
        self.__keyboard_and_statistic[keyboard] = KeyboardStatistic()

    def add_speed(self, keyboard, daytime):
        self.__keyboard_and_statistic[keyboard].add_speed(daytime, self.__user.password)

    def add_pressed_key(self, keyboard, pressed_key):
        self.__keyboard_and_statistic[keyboard].add_pressed_key(pressed_key)

    def add_pressed_time(self, keyboard, pressed_time):
        self.__keyboard_and_statistic[keyboard].add_pressed_time(pressed_time)

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

    def calculate_input_dynamic(self, keyboard):
        chair_pairs = self.get_char_pairs_from_password()
        time_pairs = self.keyboard_and_statistic[keyboard].calculate_input_dynamic(self.__user.password)
        return chair_pairs, time_pairs

    def calculate_mean_speed(self, keyboard):
        return self.__keyboard_and_statistic[keyboard].calculate_mean_speed()

    def calculate_var_speed(self, keyboard):
        return self.__keyboard_and_statistic[keyboard].calculate_var_speed()

    def calculate_speed(self, start_time, end_time):
        speed = len(self.__user.password) / (end_time - start_time)
        return speed

    def get_char_pairs_from_password(self):
        return [self.__user.password[i] + "-" + self.__user.password[i + 1]
                for i in range(len(self.__user.password) - 1)]

    def init_pressed_released_key_times_dict(self, keyboard):
        self.__keyboard_and_statistic[keyboard].init_pressed_released_key_times_dict(self.__user.password)

    def add_pressed_released_key_time_el(self, keyboard, char, pressed_or_released_time):
        if not len(self.__keyboard_and_statistic[keyboard].pressed_released_key_times):
            self.init_pressed_released_key_times_dict(keyboard)
        self.__keyboard_and_statistic[keyboard].add_pressed_released_key_time_el(char, pressed_or_released_time)

    def calculate_key_hold(self, keyboard):
        return self.__keyboard_and_statistic[keyboard].calculate_key_hold()

    def pressed_keys_clear(self, keyboard):
        if self.__keyboard_and_statistic.get(keyboard, None):
            self.__keyboard_and_statistic[keyboard].pressed_keys_clear()

    def pressed_times_clear(self, keyboard):
        if self.__keyboard_and_statistic.get(keyboard, None):
            self.__keyboard_and_statistic[keyboard].pressed_times_clear()


