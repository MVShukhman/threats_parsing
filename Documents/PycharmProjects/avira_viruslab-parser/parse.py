import asyncio
import json
import requests
from bs4 import BeautifulSoup
import time


def task(i):
    global data
    url = f'https://www.avira.com/en/support-virus-lab?page={str(i)}'
    code = requests.get(url).content
    soup = BeautifulSoup(code, 'html.parser')
    table = soup.find('div', {'class': 'vlab-component__table'}).find_all('a')
    for x in table:
        name = x.find('div', {'class': 'col-md-4'}).text
        name = ''.join(name.split()[1:])
        type = x.find('div', {'class': 'col-md-3'}).text
        type = ''.join(type.split()[1:])
        date = x.find_all('div', {'class': 'col-md-2'})[1].text
        date = ''.join(date.split()[1:])
        data.append({
            'name': name,
            'type': type,
            'added on': date
        })

    print(i, 'has done')


data = []

start = time.time()

for i in range(1, 267):
    task(i)

finish = time.time()
print(finish - start)
with open('data2.json', 'w') as json_file:
    json.dump(data, json_file, sort_keys=True)
