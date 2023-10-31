import lxml.etree as lxml
import re
import pickle
from importlib_resources import files

from conversion_utils.utils import xpath_find, get_xml_id

JOS_SPECIFICATIONS_PICKLE_RESOURCE = 'jos_specifications.pickle'

## Positions of lexeme-level features for each category
LEXEME_FEATURE_MAP = {'noun':{1,2},
                      'verb':{1,2},
                      'adjective':{1},
                      'adverb':{1},
                      'pronoun':{1,2,6,7,8},
                      'numeral':{1,2},
                      'preposition':{1},
                      'conjunction':{1},
                      'particle':set(),
                      'interjection':set(),
                      'abbreviation':set(),
                      'residual':{1},
                      'punctuation':set()}

## Exceptions to feature levels specified in LEXEME_FEATURE_MAP
LEVEL_EXCEPTIONS = {('pronoun', 2, 'čezme'), ('zaimek', 2, 'čezme'),
                    ('pronoun', 2, 'medme'), ('zaimek', 2, 'medme'),
                    ('pronoun', 2, 'nadme'), ('zaimek', 2, 'nadme'),
                    ('pronoun', 2, 'name'), ('zaimek', 2, 'name'),
                    ('pronoun', 2, 'obme'), ('zaimek', 2, 'obme'),
                    ('pronoun', 2, 'podme'), ('zaimek', 2, 'podme'),
                    ('pronoun', 2, 'pome'), ('zaimek', 2, 'pome'),
                    ('pronoun', 2, 'predme'), ('zaimek', 2, 'predme'),
                    ('pronoun', 2, 'skozme'), ('zaimek', 2, 'skozme'),
                    ('pronoun', 2, 'vame'), ('zaimek', 2, 'vame'),
                    ('pronoun', 2, 'zame'), ('zaimek', 2, 'zame'),
                    ('pronoun', 3, 'tadva'), ('zaimek', 3, 'tadva'),
                    ('pronoun', 4, 'tadva'), ('zaimek', 4, 'tadva'),
                    ('pronoun', 5, 'čezme'), ('zaimek', 5, 'čezme'),
                    ('pronoun', 5, 'medme'), ('zaimek', 5, 'medme'),
                    ('pronoun', 5, 'nadme'), ('zaimek', 5, 'nadme'),
                    ('pronoun', 5, 'name'), ('zaimek', 5, 'name'),
                    ('pronoun', 5, 'obme'), ('zaimek', 5, 'obme'),
                    ('pronoun', 5, 'podme'), ('zaimek', 5, 'podme'),
                    ('pronoun', 5, 'pome'), ('zaimek', 5, 'pome'),
                    ('pronoun', 5, 'predme'), ('zaimek', 5, 'predme'),
                    ('pronoun', 5, 'skozme'), ('zaimek', 5, 'skozme'),
                    ('pronoun', 5, 'vame'), ('zaimek', 5, 'vame'),
                    ('pronoun', 5, 'zame'), ('zaimek', 5, 'zame'),
                    ('pronoun', 7, 'njegov'), ('zaimek', 7, 'njegov'),
                    ('pronoun', 8, 'jaz'), ('zaimek', 8, 'jaz'),
                    ('pronoun', 8, 'on'), ('zaimek', 8, 'on'),
                    ('pronoun', 8, 'se'), ('zaimek', 8, 'se'),
                    ('pronoun', 8, 'ti'), ('zaimek', 8, 'ti')}


class Specifications:
    """JOS specifications with list of all word categories."""

    def __init__(self):
        self.categories = []
        self.codes_map = {'en':set(), 'sl':set()}

    def add_category(self, category):
        self.categories.append(category)
        
    def add_code(self, code, language):
        self.codes_map[language].add(code)

    def find_category_by_code(self, char, language):
        return next((category for category in self.categories if category.codes.get(language) == char), None)
        
    def find_category_by_name(self, name, language):
        return next((category for category in self.categories if category.names.get(language) == name), None)

    def __str__(self):
        return 'categories:{categories}'.format(categories=self.categories)


class Category:
    """JOS word category, including list of supported features."""

    def __init__(self, names, codes, *features):
        self.names = names
        self.codes = codes
        self.features = list(features)

    def add_feature(self, feature):
        self.features.append(feature)
        
    def find_feature_by_position(self, position):
        return next((feature for feature in self.features if feature.position == position), None)

    def find_feature_by_name(self, name, language):
        return next((feature for feature in self.features if feature.names.get(language) == name), None)

    def __str__(self):
        return 'names:{names}, codes:{codes}, features:{features}'.\
            format(strings=self.names, chars=self.codes, features=self.features)


class Feature:
    """JOS category-dependent features, including list of supported values."""  

    def __init__(self, names, position, lexeme_level_flag, *values):
        self.names = names
        self.position = position
        self.lexeme_level_flag = lexeme_level_flag
        self.values = list(values)

    def add_value(self, value):
        self.values.append(value)

    def find_value_by_char(self, char, language):
        return next((value for value in self.values if value.codes.get(language) == char), None)
        
    def find_value_by_name(self, name, language):
        return next((value for value in self.values if value.names.get(language) == name), None)

    def __str__(self):
        return 'names:{names}, position:{position}, level:{level}, values:{values}'.\
            format(strings=self.names, position=self.position, level='level' if self.lexeme_level_flag else 'form', values=self.values)


class Value:
    """JOS feature-dependent values."""

    def __init__(self, names, codes):
        self.codes = codes
        self.names = names

    def __str__(self):
        return 'codes:{codes}, names:{names}'.\
            format(codes=self.codes, names=self.names)


class Pair:
    """Generic pair of English and Slovene strings."""

    def __init__(self, en, sl):
        self.en = en
        self.sl = sl

    def get(self, language):
        return getattr(self, language)

    def __str__(self):
        return 'en:{en}, sl:{sl}'.format(en=self.en, sl=self.sl)


class SpecificationsParser:
    """Parser of JOS TEI specifications, yielding Specifications."""

    def parse(self, file_name):
        root = lxml.parse(file_name).getroot()
        div_elements = xpath_find(root, 'tei:div')
        specifications = Specifications()
        for div_element in div_elements:
            xml_id = get_xml_id(div_element)
            if (xml_id == 'msd.msds-sl'):
                msd_elements = xpath_find(div_element, 'tei:table/tei:row[@role="msd"]')
                for msd_element in msd_elements:
                    msd_codes = self.get_cell_pair(msd_element, 'msd')
                    specifications.add_code(msd_codes.get('en').capitalize(), 'en')
                    specifications.add_code(msd_codes.get('sl').capitalize(), 'sl')
            elif (re.match(r'^msd\..-sl', xml_id)):
                category_element = xpath_find(div_element, 'tei:table/tei:row[@role="type"]')[0]
                category_names = self.get_cell_pair(category_element, 'value')
                category_codes = self.get_cell_pair(category_element, 'code')
                category = Category(category_names, category_codes)
                specifications.add_category(category)
                feature_elements = xpath_find(div_element, 'tei:table/tei:row[@role="attribute"]')
                for feature_element in feature_elements:
                    feature_names = self.get_cell_pair(feature_element, 'name')
                    feature_position = int(self.get_cell(feature_element, 'position'))
                    lexeme_level_flag = feature_position in LEXEME_FEATURE_MAP[category_names.get('en')]
                    feature = Feature(feature_names, feature_position, lexeme_level_flag)
                    category.add_feature(feature)
                    value_elements = xpath_find(feature_element, 'tei:cell[@role="values"]/tei:table/tei:row[@role="value"]')
                    for value_element in value_elements:
                        value_codes = self.get_cell_pair(value_element, 'name')
                        value_names = self.get_cell_pair(value_element, 'code')
                        value = Value(value_codes, value_names)
                        feature.add_value(value)
        return specifications
        
    def get_cell(self, row, role, language=None):
        language_condition = ' and @xml:lang="' + language + '"' if language is not None else ''
        expression = 'tei:cell[@role="' + role + '"' + language_condition + ']'
        text = xpath_find(row, expression)[0].text.lower()
        if (text == 'adposition'): text = 'preposition'
        return text

    def get_cell_pair(self, row, role):
        return Pair(self.get_cell(row, role, 'en'), self.get_cell(row, role, 'sl'))


class Properties:
    """Representation of properties encoded in msds."""

    def __init__(self, category, lexeme_feature_map, form_feature_map, language):
        self.category = category
        self.lexeme_feature_map = lexeme_feature_map
        self.form_feature_map = form_feature_map
        self.language = language

    def __str__(self):
        return 'language={language}, category={category}, lexeme features={lexeme_features}, form_features={form_features}'.\
            format(language=self.language, category=self.category, lexeme_features=str(self.lexeme_feature_map), form_features=str(self.form_feature_map))

    def __eq__(self, obj):
        return isinstance(obj, Properties)\
            and self.category == obj.category\
            and self.lexeme_feature_map == obj.lexeme_feature_map\
            and self.form_feature_map == obj.form_feature_map\
            and self.language == obj.language
            

class Msd:
    """JOS msd."""  

    def __init__(self, code, language):
        self.code = code
        self.language = language

    def __str__(self):
        return 'code={code}, language={language}'.format(code=self.code, language=self.language)

    def __eq__(self, obj):
        return isinstance(obj, Msd) and self.code == obj.code and self.language == obj.language


class CustomException(Exception):
    pass

class MsdException(CustomException):
    pass

class Converter:
    """Converter between Msd and Properties objects."""

    def __init__(self, xml_file_name=None):
        if (xml_file_name is None):
            resource = files('conversion_utils.resources').joinpath(JOS_SPECIFICATIONS_PICKLE_RESOURCE)
            if (resource.is_file()):
                try:
                    with resource.open('rb') as pickle_file:
                        self.specifications = pickle.load(pickle_file)
                except:
                    exit('Could not parse specifications pickle file installed.')
            else:
                exit('No pickle installed or xml provided.')
        else:
            parser = SpecificationsParser()
            try:
                self.specifications = parser.parse(xml_file_name)
            except:
                exit('Could not parse specifications xml file provided.')

    def is_valid_msd(self, msd):
        """Verify if the Msd code is in the standard JOS set."""
        return msd.code in self.specifications.codes_map[msd.language]

    def check_valid_msd(self, msd, require_valid_flag):
        """If the Msd code is not valid, raise an exception or give a warning."""
        if (not self.is_valid_msd(msd)):
            message = 'The msd {} is unknown'.format(msd.code)
            if (require_valid_flag):
                raise MsdException(message)
            else:
                print('[WARN] ' + message)

    def msd_to_properties(self, msd, language, lemma=None, require_valid_flag=False, warn_level_flag=False):
        """Convert Msd to Properties.

        The language of the generated Properties is specified and can differ from the Msd language.

        If require_valid_flag is True, a MsdException is raised if the MSD is not in the standard
        JOS set. Otherwise only a warning is given.

        If you care about accurate level information (i.e., which properties are lexeme-level and
        which are form-level), note that some features depends on the particular lemma. For such
        features, if lemma is not provided and warn_level_flag is True, a warning will be given.

        If a MSD has dashes in place of letters for certain features, they are skipped, so that
        these features are not included in the generated Properties object.

        Parameters:
        msd(Msd): the JOS MSD to convert
        language(str): the language for the Properties object to be generated: "en" (English) or "sl" (Slovene)
        lemma(str): the lemma of the word form with the MSD
        require_valid_flag(boolean): whether to raise a MsdException or only warn if a non-standard MSD is provided
        warn_level_flag(boolean): whether to warn if cannot be sure of level of a property

        Returns:
        Properties: the result of the conversion of the Msd in the language requested

        """
        self.check_valid_msd(msd, require_valid_flag)
        category_char = msd.code[0].lower()
        value_chars = msd.code[1:]
        category = self.specifications.find_category_by_code(category_char, msd.language)
        category_name = category.names.get(language)
        feature_value_list = []
        lexeme_feature_map = {}
        form_feature_map = {}
        for (index, value_char) in enumerate(value_chars, start=1):
            if (value_char != '-'):
                feature = category.find_feature_by_position(index)
                value = feature.find_value_by_char(value_char, msd.language)
                feature_name = feature.names.get(language)
                feature_value = value.names.get(language)
                if (warn_level_flag and lemma is None and (category_name, index) in [(le[0], le[1]) for le in LEVEL_EXCEPTIONS]):
                    print('[WARN] The level (lexeme vs form) of feature (category={category}, position={position}) may be incorrect, as it is lemma-specific and no lemma has been specified.'
                          .format(category=category_name, position=index))
                level_exception_flag = (category_name, feature.position, lemma) in LEVEL_EXCEPTIONS
                lexeme_level_flag = feature.lexeme_level_flag if not level_exception_flag else not feature.lexeme_level_flag
                feature_value_list.append((feature, value))
                if (lexeme_level_flag):
                    lexeme_feature_map[feature_name] = feature_value
                else:
                    form_feature_map[feature_name] = feature_value
        return Properties(category_name, lexeme_feature_map, form_feature_map, language)

    def properties_to_msd(self, properties, language, require_valid_flag=False):
        """Convert Properties to Msd.

        The language of the generated Msd is specified and can differ from the Properties language.

        If require_valid_flag is True, a MsdException is raised if the generated MSD is not in
        the standard JOS set. Otherwise only a warning is given.

        Any skipped positions among the Properties are represented as dashes in the MSD.

        Parameters:
        properties(Properties): the properties to convert
        language(str): the language for the Msd object to be returned: "en" (English) or "sl" (Slovene)
        require_valid_flag(boolean): whether to raise a MsdException or only warn if a non-standard MSD is generated
        """
        category = self.specifications.find_category_by_name(properties.category, properties.language)
        category_char = category.codes.get(language).upper()
        feature_map = properties.lexeme_feature_map.copy()
        feature_map.update(properties.form_feature_map.copy())
        position_map = {}
        for (name, value) in feature_map.items():
            feature = category.find_feature_by_name(name, properties.language)
            value = feature.find_value_by_name(value, properties.language)
            position_map[feature.position] = value.codes.get(language)
        msd_code = category_char
        i = 0
        for position in sorted(position_map.keys()):
            i += 1
            while (i < position):
                msd_code += '-'
                i += 1
            msd_code += position_map[position]
        msd = Msd(msd_code, language)
        self.check_valid_msd(msd, require_valid_flag)
        return msd

    def translate_msd(self, msd, language):
        return self.properties_to_msd(self.msd_to_properties(msd, language), language)

    def translate_properties(self, properties, language):
        return self.msd_to_properties(self.properties_to_msd(properties, language), language)
