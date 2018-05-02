# requests #(do pobierania)
# bs4 #(do parsowania)
# import json
import requests
from bs4 import BeautifulSoup
import re

SUTTA_LINKS = 'http://sasana.pl/alfabetycznie'

TRANRSLATORS = {
        'vil': 'Piotr Jagodziński',
        'var': 'Varapanyo Bhikkhu',
        'sir': 'Siristru',
        'agr': 'Agrios',
        'kow': 'Hubert Kowalewski',
        'ltw': "Lo'tsa'wa (Dobromił Dowbór)",
        'krz': 'Janusz Krzyżowski',
    }

COLLECTIONS = {
    'DN': 'Dīgha Nikāya',
    'MN': 'Majjhima Nikāya',
    'SN': 'Saṃyutta Nikāya',
    'AN': 'Aṅguttara Nikāya',
    'KN': 'Khuddaka Nikāya',
}


def get_link_list(url):  # => [link1, link2]
    """
     (net) pobranie glownej strony (alfabetycznie)
    """
    # 1. pobranie tresci
    # response = requests.get(url)

    # 2. parsowanie tresci (wydobywanie linkow)
    # return []
    suttas_links_list = []
    response = requests.get(url)
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    table_of_contents = soup.find('div', class_='yui-content')
    for a in table_of_contents.findAll('a', href=True):
        suttas_links_list.append(a["href"])
        # suttas_links_list.append('http://sasana.pl{}'.format(a['href']))
    return suttas_links_list


def get_sutta_data_list(link_list):
    """Returns list of resultss"""
    sutta_text_list = []
    for link in link_list:
        sutta_text = get_sutta_data(link)
        sutta_text_list.append(sutta_text)
    return sutta_text_list


def get_sutta_data(link):
    """
    Results:
        results: {
            title: str,
            paragraph_list: [str...],
            link: str,
            author: str,
            collection: str,
            sutta_nr: int
        }
    """
    # Korzystamy z metody results.update, poniewaz przepisuje
    #  ona dane z jednego slownika do drugiego
    # a to oznacza, ze kod mozemy podzielic na 2 czesci
    # (jedna dla url, druga dla html) i scalic wynik w jedno.

    data = {}

    # 1. url
    data.update(get_sutta_data_from_url(link))

    # 2. html
    data.update(get_sutta_data_from_html(link))

    return data


def get_sutta_data_from_url(link):
    """
    Results:
        results: {
            link: str,
            author: str,
            collection: str,
            sutta_nr: int
        }
    """

    results = {'link': f'http://sasana.pl{link}'}

    author = TRANRSLATORS.get(parse_author_code(link))
    if author is not None:
        results['author'] = author

    collection = COLLECTIONS.get(parse_collection_code(link))
    if collection is not None:
        results['collection'] = collection

    results['sutta_nr'] = parse_sutta_nr(link)
    return results


def parse_sutta_nr(link):
    sutta_code = re.search(r'(?<=-)\d+', link)
    if sutta_code is None:
        return link
    else:
        return sutta_code.group()


def parse_author_code(link):
    match_auth = re.search(r'[a-z]{3}$', link)
    return match_auth.group()


def parse_collection_code(link):
    match_coll = re.search(r'(?<=/)\w+', link)
    return match_coll.group()


def get_sutta_data_from_html(link):
    """
    Results:
        results: {
            title: str,
            paragraph_list: [str...],
        }
    """
    # 1. pobieramy tresc strony
    # 2. parsujemy strone
    # 3. pamietaj zeby przepuszczac tylko polskie paragrafy

    results = {}
    response = requests.get(f'http://sasana.pl{link}')
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')

    results['title'] = parse_sutta_title(soup)

    results['paragraph_list'] = parse_all_paragraphs(soup)

    return results


def parse_all_paragraphs(html_parser):
    if check_page_kind(html_parser) == 'table':
        return parse_paragraph_table(html_parser)
    else:
        return parse_paragraph_list(html_parser)


def check_page_kind(html_parser):
    if html_parser.find('table') is None:
        return
        # print('No table: ', html_parser)
    else:
        paragraph_data_list = html_parser.select('table p')
        for paragraph in paragraph_data_list:
            if len(str(paragraph)) > 400:
                return 'table'


def parse_paragraph_table(html_parser):
    paragraph_list = []
    sutta_content = html_parser.select('table p')
    # print(sutta_content)
    for paragraph in sutta_content:
        if len(str(paragraph)) > 200:
            # print(paragraph)
            pl_paragraph = chcek_lang(paragraph)
            if pl_paragraph is True:
                # print(pl_paragraph)
                paragraph_list.append(paragraph)

    return paragraph_list


def parse_paragraph_list(html_parser):
    paragraph_list = []
    sutta_content = html_parser.find('div', class_='drop')
    if sutta_content is not None:
        for paragraph in sutta_content.findAll('p', style=False):
            paragraph_list.append(paragraph)
    return paragraph_list


def chcek_lang(paragraph):
    special_pl_letters = 'ąężźśćłó'
    paragraph_str = (str(paragraph.string)).lower()
    return bool(set(special_pl_letters) & set(paragraph_str))


def parse_sutta_title(html_parser):
    title_content_data = html_parser.find('div', class_='page-title')
    title_content = title_content_data.find('span')
    title_content_string = title_content.string
    title_match = re.search(r'(?<=-.|–.).+\w', title_content_string)
    if title_match is None:
        print("I can't find title: ", title_content)
        return title_match
    else:
        title = title_match.group()
        return title


# get_sutta_data_from_url(SUTTA_LINKS)

def run_it():
    # print(get_link_list(SUTTA_LINKS))
    # print(get_link_list(SUTTA_LINKS)[0])
    # print(parse_sutta_nr(get_link_list(SUTTA_LINKS)[0]))
    print(get_sutta_data_list(get_link_list(SUTTA_LINKS)))


run_it()
