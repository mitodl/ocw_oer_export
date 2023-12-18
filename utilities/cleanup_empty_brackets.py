import re
def cleanup_empty_brackets(string):
    pattern = re.compile('{{}}')
    return re.sub(pattern, '', string)