"""Convert the MSD and/or syntactic dependency tags in a CoNLL-U file from English to Slovene tags.

This script was developed in the context of a specific task and may not generalise as expected. Use at your own risk.
"""

import argparse
import codecs
import lxml.etree as lxml
from importlib_resources import files

from conversion_utils.jos_msds_and_properties import Converter, Msd


def get_syn_map():
    dict_file_name = files('conversion_utils.resources').joinpath('dict.xml')
    dict_file = codecs.open(dict_file_name, 'r')
    root = lxml.parse(dict_file).getroot()
    dict_file.close() 
    return {syn.get('en'):syn.get('sl') for syn in root.xpath('syns/syn')}
    

def translate(input_file_name, scope, output_file_name):

    syn_map = get_syn_map()

    output_file = codecs.open(output_file_name, 'w')
    input_file = codecs.open(input_file_name, 'r')

    converter = Converter()

    for line in input_file:
        columns = line.strip().split('\t')
        if (len(columns) != 10):
            output_file.write(line)
        else:
            if (scope in {'msd', 'both'}):
                columns[4] = converter.translate_msd(Msd(columns[4], 'en'), 'sl').code
            if (scope in {'dep', 'both'}):
                columns[7] = syn_map[columns[7]]
            output_file.write('\t'.join(columns) + '\n')

    input_file.close()
    output_file.close()


if (__name__ == '__main__'):

    arg_parser = argparse.ArgumentParser(description='Translate JOS msds and dependency labels.')
    arg_parser.add_argument('-infile', type=str, help='Input conllu')
    arg_parser.add_argument('-scope', type=str, options=['msd', 'dep', 'both'], default='both', help='Input conllu')
    arg_parser.add_argument('-outfile', type=str, help='Output conllu')
    arguments = arg_parser.parse_args()
    input_file_name = arguments.infile
    output_file_name = arguments.outfile

    translate(input_file_name, output_file_name)
