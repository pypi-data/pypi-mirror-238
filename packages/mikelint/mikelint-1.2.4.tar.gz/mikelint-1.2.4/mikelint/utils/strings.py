"""
String helper functions
"""
import textwrap


def indent(multiline_str: str, indented=4):
    """
    Converts a multiline string to an indented string

    Args:
        multiline_str: string to be converted
        indented: number of space used for indentation

    Returns: Indented string
    """
    return textwrap.indent(multiline_str, " " * indented)


def new_line(string: str):
    """
    Append a new line at the end of the string

    Args:
        string: String to make a new line on

    Returns: Same string with a new line character
    """
    return string + "\n"
