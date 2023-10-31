"""Convert a TEI file to a XML file of the CJVT standard schema.

This script was developed in the context of a specific task and may not generalise as expected. Use at your own risk.
"""

import argparse
import lxml.etree as lxml

from conversion_utils.utils import xpath_find, TEI_NAMESPACE_QUALIFIER


def get_parsed_unit_string(parsed_unit):
    elements = xpath_find(parsed_unit, 'tei:w|tei:pc')
    return ''.join([e.text if e.get('join') == 'right' else e.text + ' ' for e in elements]).strip()


def convert(input_file_name, output_file_name):

    output_root = lxml.Element('dictionary')

    parser = lxml.XMLParser(remove_blank_text=True)
    input_root = lxml.parse(input_file_name, parser).getroot()
    parsed_units = xpath_find(input_root, 'tei:text/tei:body/tei:p/tei:s')

    for parsed_unit in parsed_units:
        entry = lxml.SubElement(output_root, 'entry')
        head = lxml.SubElement(entry, 'head')
        headword = lxml.SubElement(head, 'headword')
        lemma_text = get_parsed_unit_string(parsed_unit)
        lemma = lxml.SubElement(headword, 'lemma')
        lemma.text = lemma_text
        lexical_unit = lxml.SubElement(head, 'lexicalUnit')
        tokens = xpath_find(parsed_unit, 'tei:w|tei:pc')
        if (len(tokens) == 1):
            token = tokens[0]
            lexical_unit.set('type', 'single')
            lexeme = lxml.SubElement(lexical_unit, 'lexeme')
            if (token.tag == TEI_NAMESPACE_QUALIFIER + 'w'):
                lexeme.set('lemma', token.get('lemma'))
            lexeme.set('msd', token.get('ana')[len('mte:'):])
            lexeme.text = token.text
        else:
            lexical_unit.set('type', 'MWE')
            for (index, token) in enumerate(tokens, start=1):
                component = lxml.SubElement(lexical_unit, 'component')
                component.set('num', str(index))
                lexeme = lxml.SubElement(component, 'lexeme')
                if (token.tag == TEI_NAMESPACE_QUALIFIER + 'w'):
                    lexeme.set('lemma', token.get('lemma'))
                lexeme.set('msd', token.get('ana')[len('mte:'):])
                lexeme.text = token.text
        lexical_unit.set('structure_id', str(parsed_unit.get('structure_id')))
        body = lxml.SubElement(entry, 'body')
        senseList = lxml.SubElement(body, 'senseList')

    output_tree = lxml.ElementTree(output_root)
    output_tree.write(output_file_name, encoding='UTF-8', pretty_print=True)


if (__name__ == '__main__'):
    arg_parser = argparse.ArgumentParser(description='Convert TEI to dictionary xml.')
    arg_parser.add_argument('-infile', type=str, help='Input TEI xml')
    arg_parser.add_argument('-outfile', type=str, help='Output xml in standard cjvt schema')
    arguments = arg_parser.parse_args()
    input_file_name = arguments.infile
    output_file_name = arguments.outfile
    convert(input_file_name, output_file_name)
