from configuration_utils import check_borders, check_points, get_config


class Configuration:
    """
     Store and manage maze configuration settings.
    """
    width: int = 0
    height: int = 1
    entry: dict[str, int] = {"x": 0, "y": 0}
    exit: dict[str, int] = {"x": 0, "y": 0}
    output_file: str = ""
    perfect: bool = True
    # More keys to be added?

    @classmethod
    def load_config(cls) -> bool:
        """
        Load configuration values.

        Returns:
            bool: True if the configuration was loaded successfully,
            otherwise False.
        """
        try:
            config = get_config()
        except ConfigError as error:
            print(error)
            return False
        number_of_keys = 0
        for key, value in config.items():
            if hasattr(cls, key):
                setattr(cls, key, value)
                number_of_keys += 1
        if number_of_keys != 6:  # Must be changed if we add more keys
            print("Missing some keys, Please check.")
            return False
        return True

    @classmethod
    def validate_config(cls) -> bool:
        """
        Validate the loaded configuration values.

        Returns:
            bool: True if the configuration is valid,
            otherwise False.
        """
        if not cls.load_config():
            return False

        try:
            check_borders("width")
            check_borders("height")
            check_points("entry")
            check_points("exit")
        except ConfigError as error:
            print(error)
            return False
        if not isinstance(cls.perfect, bool):
            return False
        if (Configuration.entry["x"] == Configuration.exit["x"] and
                Configuration.entry["y"] == Configuration.exit["y"]):
            print("Entry and exit points can't have the same coordinates")
            return False

        return True


class ConfigError(Exception):
    """
    Exception raised for configuration errors.
    """
    pass
