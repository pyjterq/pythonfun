import requests
from bs4 import BeautifulSoup
import glob

# link = 'http://sasana.pl/mn-118-vil'
link = glob.glob('./url/sutta_url.html')


def get_sutta_data_from_html(url):
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

    response = requests.get(url)
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    # print(soup.prettify())

    # print(soup.find_all('td'))
    print(soup.find('table').name)


get_sutta_data_from_html(link)
