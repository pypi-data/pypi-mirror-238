"""Convert a series of CoNNL-U files to a TEI file.

This script was developed in the context of a specific task and may not generalise as expected. Use at your own risk.
"""


import argparse
import re
import sys
from glob import glob
from lxml import etree


class Sentence:
    def __init__(self, _id, no_ud=False, system='jos'):
        self._id = _id
        self.items = []
        self.links = []
        self.srl_links = []
        self.no_ud = no_ud
        self.system = system

    def add_item(self, token, lemma, upos, upos_other, xpos, misc):
        no_space_after = 'SpaceAfter' in misc and misc['SpaceAfter'] == 'No'
        ner = misc['NER'] if 'NER' in misc else 'O'
        self.items.append([token, lemma, upos, upos_other, xpos, no_space_after, ner])

    def add_link(self, link_ref, link_type):
        self.links.append([link_ref, link_type])

    def add_srl_link(self, link_ref, link_type):
        self.srl_links.append([link_ref, link_type])

    def as_xml(self, id_prefix=None):
        if id_prefix:
            xml_id = id_prefix + '.' + self._id
        else:
            xml_id = self._id
        base = etree.Element('s')
        set_xml_attr(base, 'id', xml_id)
        id_counter = 1

        in_seg = False
        sentence_base = base

        for item in self.items:
            token, lemma, upos, upos_other, xpos, no_space_after, ner = item

            if ner[0] == 'B':
                if in_seg:
                    sentence_base.append(base)
                in_seg = True
                base = etree.Element('seg')
                base.set('type', 'name')
                base.set('subtype', f'{ner[2:].lower()}')
            elif ner[0] == 'O':
                if in_seg:
                    sentence_base.append(base)
                    base = sentence_base
                in_seg = False

            if xpos in {'U', 'Z'}: # hmm, safe only as long as U is unused in English tagset and Z in Slovenian one
                to_add = etree.Element('pc')
            else:
                to_add = etree.Element('w')
                to_add.set('lemma', lemma)

            to_add.set('ana', 'mte:' + xpos)
            if not self.no_ud:
                if upos_other != '_':
                    to_add.set('msd', f'UposTag={upos}|{upos_other}')
                else:
                    to_add.set('msd', f'UposTag={upos}')

            set_xml_attr(to_add, 'id', "{}.{}".format(xml_id, id_counter))
            to_add.text = token

            id_counter += 1

            if no_space_after:
                to_add.set('join', 'right')

            base.append(to_add)

        if in_seg:
            sentence_base.append(base)
            base = sentence_base

        # depparsing linkGrp
        link_grp = etree.Element('linkGrp')
        link_grp.set('corresp', '#'+xml_id)
        link_grp.set('targFunc', 'head argument')
        link_grp.set('type', self.system.upper() + '-SYN')
        for link_id, item in enumerate(self.links):
            link_ref, link_type = item
            link = etree.Element('link')
            link.set('ana', self.system + '-syn:' + link_type.replace(':','_'))
            if link_ref == u'0':
                link.set('target', '#' + xml_id + ' #' + xml_id + '.' + str(link_id + 1))
            else:
                link.set('target', '#' + xml_id + '.' + link_ref + ' #' + xml_id + '.' + str(link_id + 1))
            link_grp.append(link)
        base.append(link_grp)

        # srl linkGrp
        if self.srl_links:
            link_grp = etree.Element('linkGrp')
            link_grp.set('corresp', '#' + xml_id)
            link_grp.set('targFunc', 'head argument')
            link_grp.set('type', 'SRL')
            for link_id, item in enumerate(self.srl_links):
                link_ref, link_type = item
                link = etree.Element('link')
                link.set('ana', 'srl:' + link_type.replace(':', '_'))
                if link_ref == u'0':
                    link.set('target', '#' + xml_id + ' #' + xml_id + '.' + str(link_id + 1))
                else:
                    link.set('target', '#' + xml_id + '.' + link_ref + ' #' + xml_id + '.' + str(link_id + 1))
                link_grp.append(link)
            base.append(link_grp)
        return base


class Paragraph:
    def __init__(self, _id):
        self._id = _id if _id is not None else 'no-id'
        self.sentences = []

    def add_sentence(self, sentence):
        self.sentences.append(sentence)

    def as_xml(self, id_prefix=None):
        if id_prefix:
            xml_id = id_prefix + '.' + self._id
        else:
            xml_id = self._id

        p = etree.Element('p')
        set_xml_attr(p, 'id', xml_id)

        for sent in self.sentences:
            p.append(sent.as_xml(id_prefix=id_prefix))
        return p


class TeiDocument:
    def __init__(self, _id, paragraphs=list()):
        self._id = _id
        self.paragraphs = paragraphs

    def as_xml(self):
        root = etree.Element('TEI')
        root.set('xmlns', 'http://www.tei-c.org/ns/1.0')
        set_xml_attr(root, 'lang', 'sl')

        xml_id = self._id
        if xml_id is not None:
            set_xml_attr(root, 'id', xml_id)
        
        tei_header = etree.SubElement(root, 'teiHeader')

        text = etree.SubElement(root, 'text')
        body = etree.SubElement(text, 'body')
        for para in self.paragraphs:
            body.append(para.as_xml(id_prefix=xml_id))

        encoding_desc = etree.SubElement(tei_header, 'encodingDesc')
        tags_decl = etree.SubElement(encoding_desc, 'tagsDecl')
        namespace = etree.SubElement(tags_decl, 'namespace')
        namespace.set('name', 'http://www.tei-c.org/ns/1.0')
        for tag in ['p', 's', 'pc', 'w']:
            count = int(text.xpath('count(.//{})'.format(tag)))
            tag_usage = etree.SubElement(namespace, 'tagUsage')
            tag_usage.set('gi', tag)
            tag_usage.set('occurs', str(count))
        return root

    def add_paragraph(self, paragraph):
        self.paragraphs.append(paragraph)
        

def build_tei_etrees(documents):
    elements = []
    for document in documents:
        elements.append(document.as_xml())
    return elements


def set_xml_attr(node, attribute, value):
    node.attrib['{http://www.w3.org/XML/1998/namespace}' + attribute] = value


def parse_metaline(line):
    tokens = line.split('=', 1)
    key = tokens[0].replace('#', '').strip()
    if len(tokens) > 1 and not tokens[1].isspace():
        val = tokens[1].strip()
    else:
        val = None
    return (key, val)


def is_metaline(line):
    if re.match('# .+ =.*', line):
        return True
    return False


def construct_tei_documents(conllu_lines):
    documents = []

    doc_id = None
    document_paragraphs  = []

    para_id = None
    para_buffer = []

    for line in conllu_lines:
        if is_metaline(line):
            key, val = parse_metaline(line)
            if key == 'newdoc id':
                if len(para_buffer) > 0:
                    document_paragraphs.append(construct_paragraph(para_id, para_buffer))
                if len(document_paragraphs) > 0:
                    documents.append(
                        TeiDocument(doc_id, document_paragraphs))
                    document_paragraphs = []
                doc_id = val
            elif key == 'newpar id':
                if len(para_buffer) > 0:
                    document_paragraphs.append(construct_paragraph(para_id, para_buffer))
                    para_buffer = []
                para_id = val
            elif key == 'sent_id':
                para_buffer.append(line)
        else:
            if not line.isspace():
                para_buffer.append(line)

    if len(para_buffer) > 0:
        document_paragraphs.append(construct_paragraph(para_id, para_buffer))

    if len(document_paragraphs) > 0:
        documents.append(
            TeiDocument(doc_id, document_paragraphs))

    return documents


def construct_paragraph(para_id, conllu_lines):
    para = Paragraph(para_id)

    sent_id = None
    sent_buffer = []

    for line in conllu_lines:
        if is_metaline(line):
            key, val = parse_metaline(line)
            if key == 'sent_id':
                if len(sent_buffer) > 0:
                    para.add_sentence(construct_sentence(sent_id, sent_buffer))
                    sent_buffer = []
                sent_id = val
        elif not line.isspace():
           sent_buffer.append(line) 

    if len(sent_buffer) > 0:
        para.add_sentence(construct_sentence(sent_id, sent_buffer))

    return para


def construct_sentence(sent_id, lines):
    sentence = Sentence(sent_id)
    for line in lines:
        if line.startswith('#') or line.isspace():
            continue
        line = line.replace('\n', '')
        tokens = line.split('\t')
        word_id = tokens[0]
        token = tokens[1]
        lemma = tokens[2]
        upos = tokens[3]
        xpos = tokens[4]
        upos_other = tokens[5]
        depparse_link = tokens[6]
        depparse_link_name = tokens[7]
        misc = {el.split('=')[0]: el.split('=')[1] for el in tokens[9].split('|')} if tokens[9] != '_' else {}

        sentence.add_item(
                token,
                lemma,
                upos,
                upos_other,
                xpos,
                misc)

        sentence.add_link(
            depparse_link,
            depparse_link_name)

        if 'SRL' in misc:
            sentence.add_srl_link(
                depparse_link,
                misc['SRL'])
    return sentence


def construct_tei_etrees(conllu_lines):
    documents = construct_tei_documents(conllu_lines)
    return build_tei_etrees(documents)


def convert_file(input_file_name, output_file_name):
    input_file = open(input_file_name, 'r')
    root = construct_tei_etrees(input_file)[0]
    tree = etree.ElementTree(root)
    tree.write(output_file_name, encoding='UTF-8', pretty_print=True)
    input_file.close()

    tree = etree.ElementTree(root)
    tree.write(output_file_name, pretty_print=True, encoding='utf-8')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Convert CoNNL-U to TEI.')
    parser.add_argument('files', nargs='+', help='CoNNL-U file')
    parser.add_argument('-o', '--out-file', dest='out', default=None, help='Write output to file instead of stdout.')
    parser.add_argument('-s', '--system', dest='system', default='jos', choices=['jos', 'ud'])

    args = parser.parse_args()

    if args.out:
        f_out = open(args.out, 'w')
    else:
        f_out = sys.stdout

    system = args.system

    for arg in args.files:
        filelist = glob(arg)
        for f in filelist:
            with open(f, 'r') as conllu_f:
                tei_etrees = construct_tei_etrees(conllu_f)
            for tei_etree in tei_etrees:
                f_out.write(etree.tostring(tei_etree, pretty_print=True, encoding='utf-8').decode())
                f_out.write('')
