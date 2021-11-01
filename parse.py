import requests
from bs4 import BeautifulSoup


URL = 'https://kolesa.kz/cars/dodge/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0',
           'accept': "*/*"}
HOST = 'https://kolesa.kz'

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='row')

    cars = []
    for item in items:
        title = item.find('span', class_='a-el-info-title')
        if title:
            title = title.get_text(strip=True)
        else:
            continue
        cars.append({
            'title': title,
             'link': HOST + item.find('a', class_='list-link').get('href'),
             'price': item.find('span', class_='price').get_text(strip=True).replace(u'\xa0', u' '),
             'description':  item.find('div', class_='a-search-description').get_text(strip=True),
             'region':  item.find('div', class_='list-region').get_text(strip=True),
             'date':  item.find('span', class_='date').get_text(strip=True)

        })
        return cars


def parse():
    html = get_html(URL)
    if html.status_code == 200:
       cars = get_content(html.text)

    else:
        print('Error')


parse()

