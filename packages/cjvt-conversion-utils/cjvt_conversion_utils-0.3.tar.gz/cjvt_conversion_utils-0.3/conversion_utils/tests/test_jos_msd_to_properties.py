import unittest

from conversion_utils.jos_msds_and_properties import Converter, Msd, MsdException

class JosMsdToPropertiesTestCase(unittest.TestCase):

    def setUp(self):
        self.converter = Converter()

    def test_en_en(self):
        properties = self.converter.msd_to_properties(Msd('Ncfpd', 'en'), 'en')
        self.assertEqual(properties.language, 'en')
        self.assertEqual(properties.category, 'noun')
        self.assertEqual(properties.lexeme_feature_map, {'type':'common', 'gender':'feminine'})
        self.assertEqual(properties.form_feature_map, {'number':'plural', 'case':'dative'})

    def test_en_sl(self):
        properties = self.converter.msd_to_properties(Msd('Ncfpd', 'en'), 'sl')
        self.assertEqual(properties.language, 'sl')
        self.assertEqual(properties.category, 'samostalnik')
        self.assertEqual(properties.lexeme_feature_map, {'vrsta':'občno_ime', 'spol':'ženski'})
        self.assertEqual(properties.form_feature_map, {'število':'množina', 'sklon':'dajalnik'})

    def test_sl_en(self):
        properties = self.converter.msd_to_properties(Msd('Sozmd', 'sl'), 'en')
        self.assertEqual(properties.language, 'en')
        self.assertEqual(properties.category, 'noun')
        self.assertEqual(properties.lexeme_feature_map, {'type':'common', 'gender':'feminine'})
        self.assertEqual(properties.form_feature_map, {'number':'plural', 'case':'dative'})

    def test_sl_sl(self):
        properties = self.converter.msd_to_properties(Msd('Sozmd', 'sl'), 'sl')
        self.assertEqual(properties.language, 'sl')
        self.assertEqual(properties.category, 'samostalnik')
        self.assertEqual(properties.lexeme_feature_map, {'vrsta':'občno_ime', 'spol':'ženski'})
        self.assertEqual(properties.form_feature_map, {'število':'množina', 'sklon':'dajalnik'})

    def test_exception_feature_level(self):
        properties = self.converter.msd_to_properties(Msd('Pp2-sd--y', 'en'), 'sl', 'ti')
        self.assertEqual(properties.language, 'sl')
        self.assertEqual(properties.category, 'zaimek')
        self.assertEqual(properties.lexeme_feature_map, {'vrsta':'osebni', 'oseba':'druga'})
        self.assertEqual(properties.form_feature_map, {'število':'ednina', 'sklon':'dajalnik', 'naslonskost':'klitična'})

    def test_normal_feature_level(self):
        properties = self.converter.msd_to_properties(Msd('Px------y', 'en'), 'sl', 'jst')
        self.assertEqual(properties.language, 'sl')
        self.assertEqual(properties.category, 'zaimek')
        self.assertEqual(properties.lexeme_feature_map, {'vrsta':'povratni', 'naslonskost':'klitična'})
        self.assertEqual(properties.form_feature_map, {})

    def test_featureless(self):
        properties = self.converter.msd_to_properties(Msd('U', 'sl'), 'en')
        self.assertEqual(properties.language, 'en')
        self.assertEqual(properties.category, 'punctuation')
        self.assertEqual(properties.lexeme_feature_map, {})
        self.assertEqual(properties.form_feature_map, {})

    def test_good_msd_with_require_valid(self):
        properties = self.converter.msd_to_properties(Msd('Ncfpd', 'en'), 'en', require_valid_flag=True)
        self.assertEqual(properties.language, 'en')
        self.assertEqual(properties.category, 'noun')
        self.assertEqual(properties.lexeme_feature_map, {'type':'common', 'gender':'feminine'})
        self.assertEqual(properties.form_feature_map, {'number':'plural', 'case':'dative'})

    def test_bad_msd(self):
        properties = self.converter.msd_to_properties(Msd('N---d', 'en'), 'en')
        self.assertEqual(properties.language, 'en')
        self.assertEqual(properties.category, 'noun')
        self.assertEqual(properties.lexeme_feature_map, {})
        self.assertEqual(properties.form_feature_map, {'case':'dative'})

    def test_bad_msd_with_require_valid(self):
        try:
            self.converter.msd_to_properties(Msd('N---d', 'en'), 'en', require_valid_flag=True)
            fails = False
        except MsdException:
            fails = True
        self.assertEqual(fails, True)
