import requests
from bs4 import BeautifulSoup
import re

# r = requests.get('https://moscow.drom.ru/auto/used/all/')
#
# soup = BeautifulSoup(r.text, 'html.parser')
#
# print(soup.find('a', class_='erw2ohd2').text)
# for link in soup.find_all('a', class_='erw2ohd2'):
#     print(link.get('href'))


r = requests.get('https://moscow.drom.ru/volkswagen/touareg/36339572.html')

soup = BeautifulSoup(r.text, 'html.parser')

print(soup.find('div', class_='e162wx9x0').text)
print(soup.find('div', class_='b-media-cont_margin_b-size-xxs').text)

for s in soup.find_all('div', class_='b-media-cont_margin_b-size-xxs'):
    span = s.find('span').text
    print(s.text)
    s.span.decompose()
    if span == 'Двигатель:' :
        engine = s.text
    elif span == 'Мощность:':
        print('tew')
    elif span == 'Трансмиссия:':
        transmission = s.text
    elif span == 'Привод:':
        drive_unit = s.text
    elif span == 'Цвет:':
        color = s.text
    elif span == 'Пробег, км:':
        mileage = s.text
    elif span =
        Steering = s.text
