# from configuration_utils import check_borders, check_points, get_config
from typing import Any

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
        return True


class ConfigError(Exception):
    pass


def get_config() -> dict[str, Any]:
    """
    Parse configuration lines into a dictionary and validate them for errors.

    Returns:
        dict[str, Any]: Dictionary of configuration key-value pairs.
    """
    # from configuration import ConfigError

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
        if key in ["ENTRY", "EXIT"]:
            value = convert_point(key, value)
        if key == "PERFECT":
            value = bool(value)
        if len(pair) > 2:
            raise ConfigError("Wrong Key=Value format.")
        if key in config.keys():
            raise ConfigError(f"Can't have two pairs of {key},"
                              f" Please remove one.")
        config[key.lower()] = value

    return config


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


def convert_point(point: str, value: str) -> dict[str, int] | None:

    value = value.split(",")
    try:
        converted_point = {
            "x": int(value[0]),
            "y": int(value[1])
        }
    except ValueError:
        print(f"Wrong data type for {point} point,"
              f" It must contain integers")
        return None
    return converted_point


def check_borders(border: str) -> None:
    # from configuration import Configuration, ConfigError

    # print(Configuration.width)
    attribute = getattr(Configuration, border)
    if isinstance(attribute, int):
        if attribute < 1:
            raise ConfigError(f"Wrong Value for {border},"
                              f" It must be greater than zero.")
    else:
        raise ConfigError(f"Wrong data type for {border},"
                          f"It must be integer")


def check_points(point: str) -> None:
    # from configuration import Configuration, ConfigError

    attribute = getattr(Configuration, point)
    if attribute["x"] >= Configuration.width:
        raise ConfigError(f"{point} point's width can't be"
                          f" greater than maze's width")
    if attribute["y"] >= Configuration.height:
        raise ConfigError(f"{point} point's height can't be"
                          f" greater than maze's height")

def main() -> None:

    print(Configuration.validate_config())
    print(Configuration.width)
    # print(Configuration.height)
    #
    # print(Configuration.entry)
    # print(Configuration.exit)
    # print(Configuration.output_file)
    # print(Configuration.perfect)


if __name__ == "__main__":
    main()

