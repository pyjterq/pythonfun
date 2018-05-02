import requests
from bs4 import BeautifulSoup
# import glob

link = 'http://sasana.pl/mn-001-vil'
response = requests.get(link)
html_doc = response.text
soup = BeautifulSoup(html_doc, 'html.parser')


def parse_paragraph_table(html_parser):
    sutta_content = html_parser.select("table p")
    # print(sutta_content)
    for paragraph in sutta_content:
        paragraph_str = str(paragraph)
        if len(paragraph_str) > 400:
            print(len(paragraph_str), paragraph_str)
    # if sutta_content is not None:
    #     for paragraph_data in sutta_content.findAll('p', style=False):
    #         print(paragraph_data)
    # for paragraph_data in sutta_content:
    #     paragraph = paragraph_data.find('p')
    #     # print(paragraph)
    #     pl_paragraph = chcek_lang(paragraph)
    #     if pl_paragraph is True:
    #         return paragraph


parse_paragraph_table(soup)

# link = glob.glob('./url/sutta_url.html')
#
#
# def get_sutta_data_from_html(url):
#     """
#     Results:
#         results: {
#             title: str,
#             paragraph_list: [str...],
#         }
#     """
#     # 1. pobieramy tresc strony
#     # 2. parsujemy strone
#     # 3. pamietaj zeby przepuszczac tylko polskie paragrafy
#
#     response = requests.get(url)
#     html_doc = response.text
#     soup = BeautifulSoup(html_doc, 'html.parser')
#     # print(soup.prettify())
#
#     # print(soup.find_all('td'))
#     print(soup.find('table').name)
#
#
# get_sutta_data_from_html(link)
