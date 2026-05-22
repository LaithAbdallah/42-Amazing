from typing import Any


class Configuration:
    """
     Store and manage maze configuration settings.
    """
    width: int = 0
    height: int = 0
    entry: tuple[int, int] = (0,0)
    exit: tuple[int, int] = (0,0)
    output_file: str = ""
    perfect: bool = True
    # More keys to be added?

    @classmethod
    def set_config(cls) -> bool:
        """
        Load and validate configuration values.

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
            if hasattr(Configuration, key):
                setattr(Configuration, key, value)
                number_of_keys += 1
        if number_of_keys != 6:  # Must be changed if we add more keys
            print("Missing some keys, Please check.")
            return False
        return True


class ConfigError(Exception):
    pass


def read_config() -> list[str]:
    """
    Read lines from config.txt while ignoring empty and commented lines.

    Returns:
         list[str]: Filtered Configuration lines.
    """
    with open("config.txt", "r") as file:
        lines_read = file.readlines()
        lines_read = list(map(lambda line: line.strip(" \n"), lines_read))
        lines_read = list(filter(lambda line: line, lines_read))
        lines_read = list(filter(lambda line: line[0] != "#", lines_read))
    return lines_read


def get_config() -> dict[str, Any]:
    """
    Parse configuration lines into a dictionary and validate them for errors.

    Returns:
        dict[str, Any]: Dictionary of configuration key-value pairs.
    """
    config: dict[str, Any] = dict()
    lines = read_config()
    for line in lines:
        pair = line.replace(" ", "").split("=")
        key = pair[0]
        value = pair[1]
        try:
            value = int(pair[1])
        except ValueError:
            pass
        else:
            if value < 0:
                raise ConfigError(f"Wrong Value for {key},"
                                  f" It can't be negative.")
        if len(pair) > 2:
            raise ConfigError("Wrong Key=Value format.")
        if key in config.keys():
            raise ConfigError(f"Can't have two pairs of {key},"
                              f" Please remove one.")
        config[key.lower()] = value
    return config
