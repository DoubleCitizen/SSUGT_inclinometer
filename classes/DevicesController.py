from classes.APIController import APIController


class DevicesController:
    _vim_api_class = APIController()
    _laser_api_class = APIController()

    @classmethod
    def get_vim_api_class(cls):
        return cls._vim_api_class

    @classmethod
    def get_laser_api_class(cls):
        return cls._laser_api_class