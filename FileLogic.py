import pickle


class FileLogic:

    @staticmethod
    def save_file(path, data):
        with open(path, "wb") as file:
            pickle.dump(data, file)

    @staticmethod
    def open_file(path):
        data = None
        with open(path, "rb") as file:
            data = pickle.load(file)
        return data
