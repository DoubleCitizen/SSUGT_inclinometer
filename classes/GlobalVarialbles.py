from datetime import timedelta


class GlobalVariables:
    """Manages globally accessible variables and states.
    
    Attributes:
        _time_static (int): Elapsed static time in seconds.
        _indicator_value (any): Stores the indicator value.
    """
    _time_static = 0
    _indicator_value = None

    @classmethod
    def set_indicator_value(cls, value):
        """Sets the indicator value.
        
        Args:
            value (any): The indicator value to set.
        """
        cls._indicator_value = value

    @classmethod
    def get_indicator_value(cls):
        """Gets the indicator value.
        
        Returns:
            any: The stored indicator value.
        """
        return cls._indicator_value

    @classmethod
    def add_time_static(cls, seconds):
        """Adds seconds to the static time.
        
        Args:
            seconds (int): Number of seconds to add.
        """
        cls._time_static += seconds

    @classmethod
    def set_time_static(cls, seconds):
        """Overrides the static time entirely.
        
        Args:
            seconds (int): New static time in seconds.
        """
        cls._time_static = seconds

    @classmethod
    def get_time_static(cls):
        """Gets static time elapsed.
        
        Returns:
            int: The static time in seconds.
        """
        return cls._time_static

    @classmethod
    def get_str_time_static(cls):
        """Formats the static time into MM:SS string representation.
        
        Returns:
            str: Formatted time string.
        """
        minutes, seconds = divmod(cls._time_static, 60)
        text_time = f"{minutes:02d}:{seconds:02d}"
        return text_time
