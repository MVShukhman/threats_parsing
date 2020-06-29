from base import Base
from bs4 import BeautifulSoup as bs
import json
import requests
import pprint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

url = 'https://knowledge-base.threatlabs.comodo.com/family/Razy'
resp = requests.get(url, verify=False)
code = resp.content
soup = bs(code, 'html.parser')

block = soup.find('div', {'class': 'col-md-9 text-block'})
name = block.h1.text

ans = {
    'name': name,
    'url': url,
    'source_keyword': '',
    'info': {}
}

block = block.find('ul', {'class': 'list-unstyled'})
items = block.find_all('li')
ans['info']['also'] = [x.text for x in items]

block = soup.find('section', {'class': 'main-content'})
block = block.find('div', {'class': 'container'})
table = block.find_all('div', {'class': 'description'})

for row in table:
    section_name = row.h2.text.strip()
    section_content = {}
    items = row.find_all('tr')
    for item in items:
        item_name = item.th.text[1:].strip()
        item_content = item.td.text.strip()
        section_content[item_name] = item_content
    ans['info'][section_name] = section_content

s = ans.__repr__()

print(type(s))