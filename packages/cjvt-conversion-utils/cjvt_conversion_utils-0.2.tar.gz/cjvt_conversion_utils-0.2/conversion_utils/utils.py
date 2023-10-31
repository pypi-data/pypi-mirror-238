"""A few convenience TEI/XML constants and functions."""


TEI_NAMESPACE = 'http://www.tei-c.org/ns/1.0'
TEI_NAMESPACE_QUALIFIER = '{' + TEI_NAMESPACE + '}'
XML_ID_ATTRIBUTE_NAME = '{http://www.w3.org/XML/1998/namespace}id'


def xpath_find(element,expression):
    """Executes XPath expression, with TEI namespace."""
    return element.xpath(expression, namespaces={'tei':TEI_NAMESPACE})


def get_xml_id(element):
    """Returns the element's @xml:id attribute."""
    return element.get(XML_ID_ATTRIBUTE_NAME)
