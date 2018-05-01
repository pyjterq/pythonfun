# requests #(do pobierania)
# bs4 #(do parsowania)
import json
import requests
from bs4 import BeautifulSoup
import re
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from bot.models import Sutta

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


class Command(BaseCommand):

    def handle(self, *args, **options):
        link_list = get_link_list(SUTTA_LINKS)
        data_list = get_sutta_data_list(link_list)

        with transaction.atomic():
            save_sutta_list(data_list)


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
    soup = BeautifulSoup(response.text, 'html.parser')
    table_of_contents = soup.find('div', class_='yui-content')
    for a in table_of_contents.findAll('a', href=True):
        suttas_links_list.append(a["href"])
        # suttas_links_list.append('http://sasana.pl{}'.format(a['href']))
    return suttas_links_list


def get_sutta_data_list(link_list):
    """Returns list of dicts"""
    sutta_text_list = []
    for link in link_list:
        sutta_text = get_sutta_data(link)
        sutta_text_list.append(sutta_text)
    return sutta_text_list


def get_sutta_data(link):
    """
    Results:
        Dict: {
            title: str,
            paragraph_list: [str...],
            link: str,
            author: str,
            collection: str,
            sutta_nr: int
        }
    """
    # Korzystamy z metody dict.update, poniewaz przepisuje
    #  ona dane z jednego slownika do drugiego
    # a to oznacza, ze kod mozemy podzielic na 2 czesci
    # (jedna dla url, druga dla html) i scalic wynik w jedno.

    data = {}

    # 1. url
    data.update(get_sutta_data_from_url(link))

    # 2. html
    data.update(get_sutta_data_from_html(link))

    return data



def parse_sutta_link(link):
    return {
        'author_code': '',
        'collection_code': '',
        'sutta_nr': ''
    }




def get_sutta_data_from_url(link):
    """
    Results:
        dict: {
            link: str,
            author: str,
            collection: str,
            sutta_nr: int
        }
    """
    
    # Nazwa Dict -> results
    
    Dict= {}
    Dict['link']: f'http://sasana.pl{link}'

#   propozycja (utworz funkcje parse_author_code)
    match_auth = re.search(r'[a-z]{3}$', link)
    author_code = match_auth.group()
    
    # O(1)
    # author = TRANRSLATORS.get(author_code)
    author = TRANRSLATORS.get(parse_author_code(link))
    if author is not None:
        Dict['author'] = author
    
    # O(n)
    for code in TRANRSLATORS.keys():
        if author_code == code:
            Dict['author']: TRANRSLATORS[code]

    # do poprawki jak u gory
    match_coll = re.search(r'(?<=\/)\w+', link)
    collection_code = match_coll.group()
    for code in COLLECTIONS.keys():
        if collection_code == code:
            Dict['collection']: COLLECTIONS[code]

    # do poprawki (w sensie utworz funkcje parse_sutta_nr)
    sutta_code = re.search(r'(?<=-)\d+', link)
    sutta_nomber = sutta_code.group()
    Dict['sutta_nr'] = int(sutta_nomber)

    return Dict


    
# parse_all_paragraph
def parse_all_paragraph(html_parser):
    if check_page_kind(html_parser) == 'TABLE':
        return parse_paragraph_table(html_parser)
    else:
        return parse_paragraph_list(html_parser)


def get_sutta_data_from_html(link):
    """
    Results:
        Dict: {
            title: str,
            paragraph_list: [str...],
        }
    """
    # 1. pobieramy tresc strony
    # 2. parsujemy strone
    # 3. pamietaj zeby przepuszczac tylko polskie paragrafy

    Dict = {}
    paragraph_list = []
    response = requests.get(f'http://sasana.pl{link}')
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    
    # DO poczytania: selektory
    # div.page-title span
    title_content_data = soup.find('div', class_='page-title')
    title_content = title_content_data.find('span')
    
    
    # przykladowy tekst tytulu: 
    Abhayarājakumāra Sutta (MN.058 - Mowa do księcia Abhaya)
    
    left, right = test.split('-')
    result = right.replace(')', '').strip() # usuwa z brzegu spacje
    
    title_content_string = title_content.string
    title_match = re.search(r'(?<=-.|–.).+\w', title_content_string)
    title = title_match.group()
    Dict['title'] = title

    sutta_content = soup.find('div', class_='drop')
    if sutta_content is not None:
        for p in sutta_content.findAll('p', style=False):
            paragraph_list.append(p)

        Dict['paragraph_list'] = paragraph_list

    sutta_content = soup.find_all('td')
    if sutta_content is not None:
        for paragraf_data in sutta_content:
            paragraf = paragraf_data.find('p')
            paragraf_str = str(paragraf.string)
            # osobna funkcja np: check_lang(paragraph)
            if 'ą' in paragraf_str:
                paragraph_list.append(paragraf)
            elif 'ę' in paragraf_str:
                paragraph_list.append(paragraf)
            elif 'ł' in paragraf_str:
                paragraph_list.append(paragraf)
            elif 'ś' in paragraf_str:
                paragraph_list.append(paragraf)
            elif 'ć' in paragraf_str:
                paragraph_list.append(paragraf)
            elif 'ó' in paragraf_str:
                paragraph_list.append(paragraf)
            elif 'ż' in paragraf_str:
                paragraph_list.append(paragraf)
        Dict['paragraph_list'] = paragraph_list
        
    Dict['paragraph_list'] = parse_all_paragraph(soup)
        
    return Dict

# Programowanie Strukturalne

special_pl_letters = ['ą', 'ę', ...]

# 2, Sposob
def check_lang(text):
    normalized_text = text.lower()
    for special_letter in special_pl_letters:
        if special_letter in normalized_text:
            return True
    return False
    
# 1. Sposob
return bool(set(special_pl_letters) & set(text.lower()))

    
# MODEL:


# json.loads(sutta.content) -> buduje slownik z paragrafami

def save_sutta_list(data_list):
    """Create Sutta instance list and save it"""
    for data in data_list:
    Sutta.objects.create(
            url=data['url'],
            content=json.dumps(data['paragraph_list']),
            author=data['author'],
            collection=data['collection'],
            sutta_number=data['sutta_nr']
            # ... itd
        )
        
        
# Praca Domowa:

# 1. Napisz (wyzszego rzedu) funkcje, ktora przyjmuje funkcje i bada w jakim czasie ona sie wykona.

def task():
    result = 0
    for i in range(100000000):
        result += i
    return result

# Mozna: time

benchmark(task) zwraca slownik, gdzie: {
   "result":  wynik przekazanej funkcji do badania
   "czas wykonania": liczba albo obiekt okreslajacy czas 
}

# 2. Odswiezyc informacje o testach. Napisz kod, ktory testuje parsowanie url.
# parse_sutta_link('') -> i sprawdzasz wyniki
# Polecam zrobic ten test poza django
# unittest.main() <--- ta linia wykrywa i odpala testy
# a metody  musza sie zaczynac nazwa  --> test_




