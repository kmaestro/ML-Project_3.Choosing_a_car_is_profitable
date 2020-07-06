import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd

def next_page(text):
    soup = BeautifulSoup(text, 'html.parser')
    url = soup.find('a', class_='e24vrp31')
    if url is None:
        return False
    return url.get('href')

def car_specifications(text):
    soup = BeautifulSoup(text, 'html.parser')

    engine = power = transmission = drive_unit = color = mileage = steering = generation = price = None
    title = soup.find('h1').text.strip()
    price = re.sub(r"[^\d]", '', soup.find('div', class_='e162wx9x0').text)
    for s in soup.find_all('div', class_='b-media-cont_margin_b-size-xxs'):
        span = s.find('span').text
        s.span.decompose()
        if span == 'Двигатель:':
            engine = s.text.strip()
        elif span == 'Мощность:':
            power = re.findall(r"\d{0,3}\s[а-я].[а-я].", s.text)[0]
        elif span == 'Трансмиссия:':
            transmission = s.text.strip()
        elif span == 'Привод:':
            drive_unit = s.text.strip()
        elif span == 'Цвет:':
            color = s.text.strip()
        elif span == 'Пробег, км:':
            mileage = s.text.strip()
        elif span == 'Руль:':
            steering = s.text.strip()
        elif span == 'Поколение:':
            generation = s.text.strip()
    array = np.array([[title, engine, power, transmission, drive_unit, color, mileage, steering, generation, price]])
    return array

def scan(text):
    soup = BeautifulSoup(text, 'html.parser')
    array_car = None
    i = 0

    for link in soup.find_all('a', class_='erw2ohd2'):
        i = i + 1
        print(i)
        specification_url = requests.get(link.get('href'))
        try:
            array = car_specifications(specification_url.text)
            if array_car is None:
                array_car = array
            else:
                array_car = np.vstack((array_car, array))
        except:
            print('except: ', i)
        print(link.get('href'))
    return array_car

url = requests.get('https://moscow.drom.ru/auto/used/all/')

page = next_page(url.text)
array_car = scan(url.text)
page_i = 1
while page != False:
    page_i = page_i + 1
    print('page: ', page_i)
    url = requests.get(page)
    page = next_page(url.text)
    if page == False:
        break
    array_car = np.vstack((array_car, scan(url.text)))

    page = next_page(url.text)


df = pd.DataFrame(array_car, columns=[
    'title', 'engine', 'power', 'transmission', 'drive_unit', 'color', 'mileage', 'steering', 'generation', 'price'
])

df.to_csv('./car.csv')