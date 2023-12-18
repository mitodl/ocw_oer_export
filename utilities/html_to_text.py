import re
def html_to_text(html):
    pattern = re.compile('<.*?>')
    return re.sub(pattern, '', html)