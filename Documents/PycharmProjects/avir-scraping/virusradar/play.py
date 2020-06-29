from bs4 import BeautifulSoup
import requests
url = 'https://www.virusradar.com/en/threat_encyclopaedia/filter?page=0'
resp = requests.get(url)
code = resp.content
soup = BeautifulSoup(code, 'html.parser')
table = soup.find('div', {'id': 'vtab-20'})
rows = table.find_all('tr')[1:]
base_link = 'https://www.virusradar.com'
for x in rows:
    curr = x.find('td')
    url = '{}{}'.format(base_link, curr.a['href'])
    print(url)
    print(curr.a.text)
    a = input()