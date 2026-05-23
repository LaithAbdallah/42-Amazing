from typing import Any

def get_config() -> dict[str, Any]:
    """
    Parse configuration lines into a dictionary and validate them for errors.

    Returns:
        dict[str, Any]: Dictionary of configuration key-value pairs.
    """
    from configuration import ConfigError

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
            value = True if key == "True" else False
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
    from configuration import Configuration, ConfigError

    Configuration.load_config()
    attribute = getattr(Configuration, border)
    if isinstance(attribute, int):
        if attribute < 1:
            raise ConfigError(f"Wrong Value for {border},"
                              f" It must be greater than zero.")
    else:
        raise ConfigError(f"Wrong data type for {border},"
                          f"It must be integer")


def check_points(point: str) -> None:
    from configuration import Configuration, ConfigError

    Configuration.load_config()
    attribute = getattr(Configuration, point)
    if attribute["x"] >= Configuration.width:
        raise ConfigError(f"{point} point's width can't be"
                          f" greater than maze's width")
    if attribute["y"] >= Configuration.height:
        raise ConfigError(f"{point} point's height can't be"
                          f" greater than maze's height")
