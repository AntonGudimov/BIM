from password_strength import PasswordPolicy, PasswordStats


class Logic:
    def __init__(self):
        self.__username = ""
        self.__password = ""
        self.__speed_dict = {"morning": list(), "afternoon": list(), "evening": list(), "night": list()}
        self.__start_time = 0
        self.__end_time = 0
        self.__mean_speed_dict = {"morning": 0, "afternoon": 0, "evening": 0, "night": 0}
        self.__var_speed_dict = {"morning": 0, "afternoon": 0, "evening": 0, "night": 0}

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
    def start_time(self):
        return self.__start_time

    @property
    def end_time(self):
        return self.__end_time

    @property
    def mean_speed_dict(self):
        return self.__mean_speed_dict

    @property
    def var_speed_dict(self):
        return self.__var_speed_dict

    @user_name.setter
    def user_name(self, user_name):
        self.__username = user_name

    @password.setter
    def password(self, password):
        self.__password = password

    @start_time.setter
    def start_time(self, start_time):
        self.__start_time = start_time

    @end_time.setter
    def end_time(self, end_time):
        self.__end_time = end_time

    def add_speed(self, key, speed):
        self.__speed_dict[key].append(speed)

    def add_mean_speed(self, key, mean_speed):
        self.__mean_speed_dict[key] = mean_speed

    def add_var_speed(self, key, var_speed):
        self.__var_speed_dict[key] = var_speed

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
        speed = len(self.__password) / (self.__end_time - self.__start_time)
        self.__start_time = 0
        self.__end_time = 0
        return speed
