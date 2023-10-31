import unittest

from conversion_utils.jos_msds_and_properties import Converter, Properties

class JosPropertiesToMsdTestCase(unittest.TestCase):

    def setUp(self):
        self.converter = Converter()

    def test_en_sl(self):
        properties_en = Properties('noun', {'type':'common', 'gender':'feminine'}, {'number':'dual', 'case':'dative'}, 'en')
        properties_sl = self.converter.translate_properties(properties_en, 'sl')
        self.assertEqual(properties_sl.category, 'samostalnik')
        self.assertEqual(properties_sl.lexeme_feature_map, {'vrsta':'občno_ime', 'spol':'ženski'})
        self.assertEqual(properties_sl.form_feature_map, {'število':'dvojina', 'sklon':'dajalnik'})
        self.assertEqual(properties_sl.language, 'sl')

    def test_sl_en(self):
        properties_sl = Properties('samostalnik', {'vrsta':'občno_ime', 'spol':'ženski'}, {'število':'dvojina', 'sklon':'dajalnik'}, 'sl')
        properties_en = self.converter.translate_properties(properties_sl, 'en')
        self.assertEqual(properties_en.category, 'noun')
        self.assertEqual(properties_en.lexeme_feature_map, {'type':'common', 'gender':'feminine'})
        self.assertEqual(properties_en.form_feature_map, {'number':'dual', 'case':'dative'})
        self.assertEqual(properties_en.language, 'en')
