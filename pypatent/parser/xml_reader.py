import xml.etree.ElementTree as etree


def read_element(path, element):
    """The function loops over this element and all subelements and returns inner text."""
    element = etree.parse(path).getroot().find(element)
    text = "\n".join(element.itertext())
    return text
