from typing import Any


def get_config() -> dict[str, Any]:
    """
    Parse configuration lines into a dictionary and validate them for errors.

    Returns:
        dict[str, Any]: Dictionary of configuration key-value pairs.
    """
    from configuration.configuration import ConfigError

    config: dict[str, Any] = dict()
    lines = read_config()
    for line in lines:
        pair = line.replace(" ", "").split("=")
        key = pair[0]
        value: Any = pair[1]
        try:
            value = int(pair[1])
        except ValueError:
            pass
        if key in ["ENTRY", "EXIT"]:
            value = convert_point(key, value)
        if key == "PERFECT":
            if value == "True":
                value = True
            elif value == "False":
                value = False
            else:
                raise ConfigError("Wrong value for PERFECT key.")
        if len(pair) > 2:
            raise ConfigError("Wrong Key=Value format.")
        if key.lower() in config.keys():
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


def convert_point(point: str, value: Any) -> dict[str, int] | None:
    """
    Convert a comma-separated string into a point dictionary.

    Args:
        point: The name of the point (e.g. "ENTRY" or "EXIT").
        value: The comma-separated string to convert.

    Returns:
        dict[str, int]: The converted point dictionary with "x" and "y" keys,
        or None if the conversion fails.
    """
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
    """
    Validate that a border attribute is a positive integer.

    Args:
        border: The name of the border attribute
         to check ("width" or "height").

    Raises:
        ConfigError: If the border value is not a positive integer.
    """
    from configuration.configuration import Configuration, ConfigError

    Configuration.load_config()
    attribute = getattr(Configuration, border)

    if isinstance(attribute, int):

        if attribute < 1:
            raise ConfigError(f"Wrong Value for {border},"
                              f" It must be greater than zero.")

        if border == "width" and attribute > 55:
            raise ConfigError("Width can't be greater than 55")

        if border == "height" and attribute > 35:
            raise ConfigError("Height can't be greater than 35")

    else:
        raise ConfigError(f"Wrong data type for {border},"
                          f"It must be integer")


def check_points(point: str) -> None:
    """
    Validate that a point is within the maze's boundaries.

    Args:
        point: The name of the point attribute to check ("entry" or "exit").

    Raises:
        ConfigError: If the point's coordinates exceed the maze's dimensions.
    """
    from configuration.configuration import Configuration, ConfigError

    Configuration.load_config()
    attribute = getattr(Configuration, point)

    if attribute["x"] >= Configuration.width:
        raise ConfigError(f"{point} point's width can't be"
                          f" greater than maze's width")

    if attribute["y"] >= Configuration.height:
        raise ConfigError(f"{point} point's height can't be"
                          f" greater than maze's height")
