import unittest

from parser_html import get_sutta_data_from_url


class TestSuttaDataFromUrl(unittest.TestCase):

    def test_sutta_number(self):
        results = get_sutta_data_from_url('/mn-123-var')
        self.assertEqual((results['sutta_nr']), 123)

    def test_sutta_tittle(self):
        results = get_sutta_data_from_url('/mn-123-var')
        self.assertEqual(results['link'], 'http://sasana.pl/mn-123-var')

    def test_sutta_author(self):
        results = get_sutta_data_from_url('/mn-123-var')
        self.assertEqual(results['author'], 'Varapanyo Bhikkhu')

    def test_sutta_collection(self):
        results = get_sutta_data_from_url('/mn-123-var')
        self.assertEqual(results['collection'], 'MN')


unittest.main()
