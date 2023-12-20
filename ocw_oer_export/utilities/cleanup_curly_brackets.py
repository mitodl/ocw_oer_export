"""
Module for cleaning up content within curly brackets in a string.
"""
import re


def cleanup_curly_brackets(string):
    """Remove content within curly brackets (including the brackets) from the input string."""
    pattern = re.compile("{.*?}")
    return re.sub(pattern, "", string)
