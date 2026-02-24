import os
import json

class ConfigController:
    """Manages simple JSON configuration serialization and directory initialization.
    
    Attributes:
        path_to_project (str): Target filesystem path for the JSON config file.
    """
    def __init__(self, path_to_project: str):
        """Initializes controller, creates directories and creates empty JSON if missing.
        
        Args:
            path_to_project (str): Path to the JSON configuration file to be managed.
        """
        self.path_to_project = path_to_project
        if self.path_to_project is None:
            return
        self.path_to_project = self.path_to_project.replace('//', '/')
        self.path_to_project = self.path_to_project.replace('\\', '/')
        self.generate_directories()
        if not os.path.exists(self.path_to_project):
            with open(self.path_to_project, 'w+') as f:
                json.dump({}, f)

    def generate_directories(self):
        """Generates directories up to the config file path if they don't exist."""
        path_result = ''
        if self.path_to_project.rfind('.') != -1:
            path_without_file = self.path_to_project.split('/')[0:len(self.path_to_project.split('/')) - 1]
        else:
            path_without_file = self.path_to_project.split('/')[0:len(self.path_to_project.split('/'))]
        for path in path_without_file:
            path_result += path + '/'
            if not os.path.isdir(path_result):
                os.makedirs(path_result, exist_ok=False)

    def _load_or_create(self):
        """Loads data from the JSON file or creates it empty if missing.
        
        Returns:
            dict or list: The loaded configuration data.
        """
        if self.path_to_project is None:
            return {}
        try:
            with open(self.path_to_project, 'r') as f:
                return json.load(f)
        except IsADirectoryError:
            return {}
        except FileNotFoundError:
            return {}
        except PermissionError:
            return {}
        except BufferError:
            return {}

    def load(self) -> dict | list:
        """Loads data from the JSON configuration file.
        
        Returns:
            dict | list: The data extracted from the configuration file.
        """
        data = self._load_or_create()
        return data

    def save(self, data: dict | list):
        """Saves data back to the JSON configuration file.
        
        Args:
            data (dict | list): Content to store persistently.
        """
        if self.path_to_project is None:
            return
        with open(self.path_to_project, 'w+') as f:
            json.dump(data, f)