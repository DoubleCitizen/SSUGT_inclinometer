from classes.APIController import APIController


class DevicesController:
    """Manages APIController instances for connected devices."""
    _vim_api_class = APIController()
    _laser_api_class = APIController()

    @classmethod
    def get_vim_api_class(cls):
        """Retrieves APIController instance for the VIM device.
        
        Returns:
            APIController: VIM device controller.
        """
        return cls._vim_api_class

    @classmethod
    def get_laser_api_class(cls):
        """Retrieves APIController instance for the Laser device.
        
        Returns:
            APIController: Laser device controller.
        """
        return cls._laser_api_class