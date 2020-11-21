import numpy as np


class KeyboardStatistic:
    def __init__(self):
        self.__speed_dict = {"morning": list(), "afternoon": list(), "evening": list(), "night": list()}
        self.__pressed_keys = list()
        self.__pressed_times = list()
        self.__key_overlay_count = 0
        self.__key_overlay_count_2 = 0
        self.__key_overlay_count_3 = 0
        self.__pressed_released_key_times = dict()

    @property
    def speed_dict(self):
        return self.__speed_dict

    @property
    def key_overlay_count(self):
        return self.__key_overlay_count

    @property
    def key_overlay_count_2(self):
        return self.__key_overlay_count_2

    @property
    def key_overlay_count_3(self):
        return self.__key_overlay_count_3

    @property
    def pressed_released_key_times(self):
        return self.__pressed_released_key_times

    @key_overlay_count.setter
    def key_overlay_count(self, key_overlay_count):
        self.__key_overlay_count = key_overlay_count

    @key_overlay_count_2.setter
    def key_overlay_count_2(self, key_overlay_count_2):
        self.__key_overlay_count_2 = key_overlay_count_2

    @key_overlay_count_3.setter
    def key_overlay_count_3(self, key_overlay_count_3):
        self.__key_overlay_count_3 = key_overlay_count_3

    def add_speed(self, daytime, password):
        speed = len(password) / (self.__pressed_times[-1] - self.__pressed_times[0])
        self.__speed_dict[daytime].append(speed)

    def add_pressed_key(self, pressed_key):
        self.__pressed_keys.append(pressed_key)

    def add_pressed_time(self, pressed_time):
        self.__pressed_times.append(pressed_time)

    def init_pressed_released_key_times_dict(self, password):
        for char in password:
            self.__pressed_released_key_times[char] = list()

    def add_pressed_released_key_time_el(self, char, pressed_or_released_time):
        self.__pressed_released_key_times[char].append(pressed_or_released_time)

    # Расчет динамики ввода парольной фразы
    def calculate_input_dynamic(self, password):
        time_pairs = list()
        for i in range(len(password)):
            for j in range(i, len(self.__pressed_keys)):
                if password[i] == self.__pressed_keys[j]:
                    for k in range(j + 1, len(self.__pressed_keys)):
                        if password[i + 1] == self.__pressed_keys[k]:
                            time_pairs.append(self.__pressed_times[k] - self.__pressed_times[j])
                            break
                    break
        return time_pairs

    # Расчет математического ожидания скорости парольной фразы
    def calculate_mean_speed(self):
        mean_speed_dict = {"morning": 0.0, "afternoon": 0.0, "evening": 0.0, "night": 0.0}
        for day_time, speed in self.__speed_dict.items():
            if len(speed):
                mean_speed_dict[day_time] = np.float(np.mean(self.__speed_dict[day_time]))
        return mean_speed_dict

    # Расчет дисперсии скорости парольной фразы
    def calculate_var_speed(self):
        var_speed_dict = {"morning": 0.0, "afternoon": 0.0, "evening": 0.0, "night": 0.0}
        for day_time, speed in self.__speed_dict.items():
            if len(speed):
                var_speed_dict[day_time] = np.float(np.var(self.__speed_dict[day_time]))
        return var_speed_dict

    # Расчет времени удержания клавиш при вводе пароля
    def calculate_key_hold(self):
        pressed_released_diff = dict()
        pressed_released_diff_list = list()
        for char, pressed_release_list in self.__pressed_released_key_times.items():
            for i in range(0, len(pressed_release_list) - 1, 2):
                pressed_released_diff_list.append(
                    pressed_release_list[i + 1] - pressed_release_list[i])
            pressed_released_diff[char] = np.float(np.mean(pressed_released_diff_list))
            pressed_released_diff_list.clear()
        return pressed_released_diff

    def pressed_keys_clear(self):
        self.__pressed_keys.clear()

    def pressed_times_clear(self):
        self.__pressed_times.clear()
