"""
Utilities module with aiding functions for the main project modules
"""


def rgbToJson(rgb_list: list) -> dict:
    """
    Converts RGB values to a JSON object

    :param list rgb_list: RGB value to convert
    :return: JSON object as a dictionary
    """
    return {"r": rgb_list[0], "g": rgb_list[1], "b": rgb_list[2]}
