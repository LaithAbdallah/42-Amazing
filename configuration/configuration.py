from configuration.configuration_utils import check_borders, check_points
from configuration.configuration_utils import get_config


class Configuration:
    """
    Store and manage maze configuration settings.

    Attributes:
        width: The width of the maze in cells.
        height: The height of the maze in cells.
        entry: The entry point coordinates as {"x": col, "y": row}.
        exit: The exit point coordinates as {"x": col, "y": row}.
        output_file: The path to the output file.
        perfect: If True, the maze will have exactly one
         path between the entry and the exit.
        seed: if zero, then it will regenrate randomly every time,
         other than that it would generate the same maze using the same seed
    """

    width: int = 1
    height: int = 1
    entry: dict[str, int] = {"x": 0, "y": 0}
    exit: dict[str, int] = {"x": 0, "y": 0}
    output_file: str = ""
    perfect: bool = True
    seed: int = 0

    @classmethod
    def load_config(cls, show_exceptions: bool) -> bool:
        """
        Load configuration values.

        Args:
            show_exception: If true raise exceptions, otherwise don't

        Returns:
            bool: True if the configuration was loaded successfully,
            otherwise False.
        """
        # Seed is optional
        keys = ["width", "height", "entry", "exit", "output_file", "perfect"]
        try:
            config = get_config()
        except ConfigError as error:
            if show_exceptions:
                print(error)
            return False
        number_of_keys = 0
        for key, value in config.items():
            if hasattr(cls, key):
                setattr(cls, key, value)
                number_of_keys += 1
        for key in keys:
            if key not in config.keys():
                if show_exceptions:
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
        if not cls.load_config(False):
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
