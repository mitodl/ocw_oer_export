"""
Module for converting HTML string to plain text.
"""
import re


def html_to_text(html):
    """Remove HTML tags from an HTML string."""
    pattern = re.compile("<.*?>")
    return re.sub(pattern, "", html)
