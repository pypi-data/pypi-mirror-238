import unittest

from conversion_utils.jos_msds_and_properties import Converter, Properties, MsdException

class JosPropertiesToMsdTestCase(unittest.TestCase):

    def setUp(self):
        self.converter = Converter()

    def test_en_en(self):
        msd = self.converter.properties_to_msd(Properties('noun', {'type':'common', 'gender':'feminine'}, {'number':'dual', 'case':'nominative'}, 'en'), 'en')
        self.assertEqual(msd.language, 'en')
        self.assertEqual(msd.code, 'Ncfdn')

    def test_en_sl(self):
        msd = self.converter.properties_to_msd(Properties('noun', {'type':'common', 'gender':'feminine'}, {'number':'dual', 'case':'nominative'}, 'en'), 'sl')
        self.assertEqual(msd.language, 'sl')
        self.assertEqual(msd.code, 'Sozdi')

    def test_sl_en(self):
        msd = self.converter.properties_to_msd(Properties('samostalnik', {'vrsta':'občno_ime', 'spol':'ženski'}, {'število':'dvojina', 'sklon':'imenovalnik'}, 'sl'), 'en')
        self.assertEqual(msd.language, 'en')
        self.assertEqual(msd.code, 'Ncfdn')

    def test_sl_sl(self):
        msd = self.converter.properties_to_msd(Properties('samostalnik', {'vrsta':'občno_ime', 'spol':'ženski'}, {'število':'dvojina', 'sklon':'imenovalnik'}, 'sl'), 'sl')
        self.assertEqual(msd.language, 'sl')
        self.assertEqual(msd.code, 'Sozdi')

    def test_exception_feature_level(self):
        msd = self.converter.properties_to_msd(Properties('zaimek', {'vrsta':'osebni', 'oseba':'druga'}, {'število':'ednina', 'sklon':'dajalnik', 'naslonskost':'klitična'}, 'sl'), 'en')
        self.assertEqual(msd.language, 'en')
        self.assertEqual(msd.code, 'Pp2-sd--y')

    def test_normal_feature_level(self):
        msd = self.converter.properties_to_msd(Properties('zaimek', {'vrsta':'povratni', 'naslonskost':'klitična'}, {}, 'sl'), 'en')
        self.assertEqual(msd.language, 'en')
        self.assertEqual(msd.code, 'Px------y')

    def test_featureless(self):
        msd = self.converter.properties_to_msd(Properties('punctuation', {}, {}, 'en'), 'sl')
        self.assertEqual(msd.language, 'sl')
        self.assertEqual(msd.code, 'U')

    def test_good_msd_with_require_valid(self):
        msd = self.converter.properties_to_msd(Properties('noun', {'type':'common', 'gender':'feminine'}, {'number':'dual', 'case':'nominative'}, 'en'), 'en', require_valid_flag=True)
        self.assertEqual(msd.language, 'en')
        self.assertEqual(msd.code, 'Ncfdn')

    def test_bad_msd(self):
        msd = self.converter.properties_to_msd(Properties('noun', {'type':'common'}, {'number':'dual'}, 'en'), 'en')
        self.assertEqual(msd.language, 'en')
        self.assertEqual(msd.code, 'Nc-d')

    def test_bad_msd_with_require_valid(self):
        try:
            self.converter.properties_to_msd(Properties('noun', {'type':'common'}, {'number':'dual'}, 'en'), 'en', require_valid_flag=True)
            fails = False
        except MsdException:
            fails = True
        self.assertEqual(fails, True)
