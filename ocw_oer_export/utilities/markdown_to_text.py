from markdown import Markdown
from io import StringIO

def unmark_element(element, stream=None):
    """Helper function to recursively extract text from Markdown elements."""
    if stream is None:
        stream = StringIO()
    if element.text:
        stream.write(element.text)
    for sub in element:
        unmark_element(sub, stream)
    if element.tail:
        stream.write(element.tail)
    return stream.getvalue()

# patching Markdown
Markdown.output_formats["plain"] = unmark_element
markdown_converter = Markdown(output_format="plain")
markdown_converter.stripTopLevelTags = False


def markdown_to_text(markdown):
    """Convert Markdown to plain text using the markdown_converter."""
    return markdown_converter.convert(markdown)