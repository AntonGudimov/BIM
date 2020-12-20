import numpy as np


class KeyboardStatistic:
    def __init__(self):
        # словарь скорости ввода пароля
        # каждый элемент листа - скорость ввода пароля
        self.__speed_dict = {"morning": list(), "afternoon": list(), "evening": list(), "night": list()}
        self.__pressed_keys = list()    # лист из нажатых клавиш пароля
        self.__pressed_times = list()   # лист из времени нажатых клавиш пароля
        self.__released_keys = list()
        self.__released_times = list()
        self.__key_overlay_count = 0    # кол-во наложения 1 типа
        self.__key_overlay_count_2 = 0  # кол-во наложения 2 типа
        self.__key_overlay_count_3 = 0  # кол-во наложения 3 типа

        # словарь ввида буква пароля : [время нажатия1, время отпускания1, ..., время нажатияn, время отпусканияn]
        self.__pressed_released_key_times = dict()

        # функция f(t)
        self.__func_t = dict()

    @property
    def func_t(self):
        return self.__func_t

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

    def add_released_key(self, released_key):
        self.__released_keys.append(released_key)

    def add_released_time(self, released_time):
        self.__released_times.append(released_time)

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
        # self.__pressed_released_key_times.clear()
        return pressed_released_diff

    def pressed_keys_clear(self):
        self.__pressed_keys.clear()

    def pressed_times_clear(self):
        self.__pressed_times.clear()

    def released_keys_clear(self):
        self.__released_keys.clear()

    def released_times_clear(self):
        self.__released_times.clear()

    def pressed_released_key_times_dict_clear(self):
        self.__pressed_released_key_times.clear()

    # Функции для 2 лабы
    def add_value_to_func_t(self):
        A = 1
        k = 2
        pressed_time = self.__pressed_times[-1]

        if not len(self.__pressed_times) == 1:
            pressed_key_before = self.__pressed_keys[-2]
            pressed_time_before = self.__pressed_times[-2]

            #pressed_release_times = self.__pressed_released_key_times.get(pressed_key_before, None)
            #index = pressed_release_times.index(pressed_time_before)
            #if len(pressed_release_times) - 1 == index:
            if len(self.__released_times) != len(self.__pressed_times) - 1:
                A *= k
        self.__func_t[pressed_time] = A

    def haara_func(self, n, tk):
        r = -1
        m = 0
        if not n:
            r = 0
        else:
            log2N = n
            r_right_limit = 1
            func_value = 0
            # Определение r и m на основе n
            while True:
                for i in range(r_right_limit):
                    r += 1
                    m_right_limit = 2 ** r
                    m = 0
                    for j in range(1, m_right_limit + 1):
                        m += 1
                        log2N -= 1
                        if not log2N:
                            break
                    if not log2N:
                        break
                if not log2N:
                    break
                else:
                    r_right_limit += 1

        # Расчет функции Хаара
        if (m - 1) / (2 ** r) <= tk < (m - 0.5) / (2 ** r):
            func_value = 2 ** (r / 2)
        elif (m - 0.5) / (2 ** r) <= tk < m / (2 ** r):
            func_value = - (2 ** (r / 2))
        else:
            func_value = 0
        return func_value

    def form_vector(self, password_length):
        vector = list()
        last_pressed_key = self.__pressed_keys[-1]
        #last_released_time = self.__pressed_released_key_times.get(last_pressed_key, None)[-1]
        last_released_time = self.__released_times[-1]
        start_time = self.__pressed_times[0]
        T = last_released_time - start_time
        for i in range(password_length):
            vector_el = 0
            for j in range(len(self.__pressed_times)):
                tk = self.__pressed_times[j]
                vector_el += self.__func_t.get(tk, 0) * self.haara_func(i, (tk - start_time) / T)
            vector_el_value = vector_el / password_length
            vector.append(round(vector_el_value, 5))
        return vector


