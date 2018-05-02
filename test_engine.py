import unittest

from parser_html import get_link_list, get_sutta_data


# Test integracyjny

# import requests

# class OnlineHttpProvider:

#     def get(self, url):
#         response = requests.get(url)
#         return response.text


# class OfflineHttpProvider:

#     def get(self, url):
#         # odczyt z pliku
#         text = '<html...></html>
#         return text


# class TestGetLinkList(unittest.TestCase):
#     def test_parse_url(self):
#         http_provider = OfflineHttpProvider()  # get(url)
#         links = get_link_list(http_provider, 'http://sasana.pl/alfabetycznie')
#         self.assertGreater(len(links), 0)


# class TestGetLinkList(unittest.TestCase):
#     def test_parse_url(self):
#         links = get_link_list('http://sasana.pl/alfabetycznie')
#         self.assertGreater(len(links), 0)

# PEP8 -> snakecase

class TestGetSuttaData(test_engine.TestCase):

    def test_sutta_number(self):
        results = get_sutta_data('/mn-123-var')
        self.assertEqual((results['sutta_nr']), 123)

    def test_sutta_paragraphs(self):
        results = get_sutta_data('/mn-123-var')
        self.assertIsNotNone(results['paragraph_list'])

    def test_sutta_tittle(self):
        results = get_sutta_data('/mn-123-var')
        self.assertEqual(results['title'], 'Cudowne i Wspaniałe')

    def test_sutta_author(self):
        results = get_sutta_data('/mn-123-var')
        self.assertEqual(results['author'], 'Varapanyo Bhikkhu')


unittest.main()
