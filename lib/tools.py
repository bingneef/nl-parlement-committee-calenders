import re


def generate_safe_filename(filename):
    return re.sub(r"[ /]", "-", filename)