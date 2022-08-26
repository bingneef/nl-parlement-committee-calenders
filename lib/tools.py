import re
from bs4 import BeautifulSoup
from datetime import datetime


def current_formatted_time() -> str:
    return datetime.now().strftime("%H:%M:%S")

def generate_safe_filename(root_filename: str, extension: str) -> str:
    """
    Generate the root filename (thus without extension) stripped of unwanted characters ( /&,.)
    :param str root_filename: Filename without the extension
    :param str extension: Filename extension
    :return: The safe combined filename str
    """
    safe_root_file_name = re.sub(r"[ /&,.]", "-", root_filename)
    return f"{safe_root_file_name}.{extension}"


def text_from_html_string(text: str, separator="\n") -> str:
    """
    Fetch the text of the html string, lines separated by the separator
    :param str text: The html string
    :param separator: The separator for line breaks
    :type separator: str or None
    :return: The separated text from the html string
    """
    return BeautifulSoup(text, "lxml").get_text(separator=separator)
