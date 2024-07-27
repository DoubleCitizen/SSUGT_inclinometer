import os
from datetime import datetime


class FileSaver:
    def __init__(self):
        self.sep = ';'

    @staticmethod
    def create_directory(folder_path):
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            return
        else:
            os.makedirs(folder_path)

    def initialize(self, headers, sep=';'):
        # Получение текущего времени
        current_time = datetime.now()
        self.sep = sep

        # Форматирование времени в строку в нужном формате
        formatted_time = current_time.strftime("%Y_%m_%d %H_%M_%S")
        current_directory = os.getcwd()
        self.create_directory(current_directory.replace('\\', '/') + '/data')

        self.filename = current_directory + "/data/" + formatted_time + ".csv"
        with open(self.filename, 'w+') as file:
            file.write(f"sep={sep}\n")
            for i, header in enumerate(headers):
                if len(headers) - 1 == i:
                    file.write(str(header))
                else:
                    file.write(str(header) + self.sep)
            file.write('\n')

    def write_data(self, data: list):
        with open(self.filename, 'a') as file:
            for i, value in enumerate(data):
                if len(data) - 1 == i:
                    file.write(str(value))
                else:
                    file.write(str(value) + self.sep)
            file.write('\n')

