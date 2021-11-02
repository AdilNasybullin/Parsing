import requests
from bs4 import BeautifulSoup
import csv
import os


URL = 'https://kolesa.kz/cars/dodge/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0',
           'accept': "*/*"}
HOST = 'https://kolesa.kz'
FILE = 'cars.csv'

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    # pagination = soup.find_all('div', class_='pager').find_next('span')
    pagination = soup.find('div', class_='pager').find_all('li')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1
    # print(pagination)

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


def save_file(items, path):
    with open(path, 'w', newline='', encoding='cp1251', errors="ignore") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Марка', 'Ссылка', 'Цена', 'Описание', 'Город', 'Дата'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['price'], item['description'],
                            item['region'], item['date']])


def parse():
    URL = input('Введите URL: ')
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))
        save_file(cars, FILE)
        print(f'Получено {len(cars)} записей')
        os.startfile(FILE)

    else:
        print('Error')


parse()

