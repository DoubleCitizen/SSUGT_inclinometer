import os
import json

class ConfigController:
    def __init__(self, path_to_project: str):
        """
        :param path_to_project: путь к файлу json, в котором будет происходить сериализация/десериализация
        """
        self.path_to_project = path_to_project
        if self.path_to_project is None:
            return
        if not os.path.exists(self.path_to_project):
            with open(self.path_to_project, 'w+') as f:
                json.dump({}, f)

    def _load_or_create(self):
        """
        Подгружает данные из файла json или создает его пустым, если он отсутствует.
        :return: загруженные данные
        """
        if self.path_to_project is None:
            return {}
        try:
            with open(self.path_to_project, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def load(self) -> dict | list:
        """
        :return: Данные (dict | list)
        Загрузка данных из файла json (dict | list)
        """
        data = self._load_or_create()
        return data

    def save(self, data: dict | list):
        """
        :param data: Входные данные (dict | list)
        Сохранение данных в файл json (dict | list)
        """
        if self.path_to_project is None:
            return
        with open(self.path_to_project, 'w+') as f:
            json.dump(data, f)