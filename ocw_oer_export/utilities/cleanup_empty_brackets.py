import re

def cleanup_empty_brackets(string):
    """Remove content within curly brackets (including the brackets) from the input string."""
    pattern = re.compile('{.*?}')
    return re.sub(pattern, '', string)
