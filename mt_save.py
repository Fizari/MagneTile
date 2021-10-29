import os

class Save:

    save_filename = "save"
    save_fullpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), save_filename)

    def __init__(self):
        pass

    def save_highscore(self, score):
        data = str(score)
        self.__write_to_save_file(data)

    def get_highscore(self):
        data = self.__read_from_save_file()
        if data and data != "":
            return int(data)
        return None

    def __write_to_save_file(self, data):
        f = open(self.save_fullpath, "w")
        f.write(data)
        f.close()

    def __read_from_save_file(self):
        f = open(self.save_fullpath, "r")
        data = f.read()
        f.close()
        return data
