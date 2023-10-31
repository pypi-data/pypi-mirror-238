import unittest

from conversion_utils.jos_msds_and_properties import Converter, Msd

class JosMsdToPropertiesTestCase(unittest.TestCase):

    def setUp(self):
        self.converter = Converter()

    def test_en_sl(self):
        msd_sl = self.converter.translate_msd(Msd('Ncfpd', 'en'), 'sl')
        self.assertEqual(msd_sl.language, 'sl')
        self.assertEqual(msd_sl.code, 'Sozmd')

    def test_sl_en(self):
        msd_en = self.converter.translate_msd(Msd('Sozmd', 'sl'), 'en')
        self.assertEqual(msd_en.language, 'en')
        self.assertEqual(msd_en.code, 'Ncfpd')
