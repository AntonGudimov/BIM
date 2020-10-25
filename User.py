class User:
    def __init__(self):
        self.__login = ""
        self.__password = ""

    @property
    def login(self):
        return self.__login

    @property
    def password(self):
        return self.__password

    @login.setter
    def login(self, login):
        self.__login = login

    @password.setter
    def password(self, password):
        self.__password = password


