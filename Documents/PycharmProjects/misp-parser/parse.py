import requests
import json
from bs4 import BeautifulSoup
f = open('code.html', 'r')
code = f.read()
soup = BeautifulSoup(code, 'html.parser')
elems = soup.find_all('div', {'class': 'sect2'})
storage = {}
for curr in elems:
    name = curr.find('a', {'class': 'link'}).text
    storage[name] = {}
    divs = curr.find_all('div')
    elem_info = ''
    for i, x in enumerate(divs):
        if 'The tag is:' in x.text:
            pos = x.text.find('=')
            tag = x.text[pos+2:-3]
            storage[name]['tag'] = tag
            continue
        if 'ulist' in x['class']:
            key = None
            if 'relationships with:' in divs[i - 1].text:
                key = 'relationships'
            elif 'known as:' in divs[i - 1].text:
                key = 'known as'
            if key is None:
                elem_info += x.text
            else:
                storage[name][key] = [temp.text for temp in x.find_all('li')]
        elif 'relationships with:' not in x and 'known as:' not in x:
            elem_info += x.text

    storage[name]['info'] = elem_info

    table = curr.find_all('td')
    if len(table) != 0:
        storage[name]['links'] = [x.text for x in table[1:]]

with open('data.json', 'w') as json_file:
    json.dump(storage, json_file, sort_keys=True)




