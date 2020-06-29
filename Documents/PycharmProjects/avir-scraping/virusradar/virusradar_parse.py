from bs4 import BeautifulSoup
import json
import requests
import os


class VirusradarParser:
    main_url = 'https://www.virusradar.com/en/threat_encyclopaedia/filter?page='
    keyname = 'virusradar'
    storage = []
    links = []

    def __init__(self):
        self.__get_links()

    def __get_links(self):
        filename = '{}_links.json'.format(self.keyname)
        if not os.path.exists(filename):
            with open(filename, 'w') as json_file:
                base_link = 'https://www.virusradar.com'
                for i in range(244):
                    url = '{}{}'.format(self.main_url, str(i))
                    resp = requests.get(url)
                    code = resp.content
                    soup = BeautifulSoup(code, 'html.parser')
                    table = soup.find('div', {'id': 'vtab-20'})
                    rows = table.find_all('tr')[1:]
                    for row in rows:
                        curr = row.find('td')
                        url = '{}{}'.format(base_link, curr.a['href'])
                        name = curr.a.text
                        self.links.append({
                            'name': name,
                            'link': url
                        })

                    print(i)

                json.dump(self.links, json_file)
        else:
            with open(filename, 'r') as json_file:
                self.links = json.load(json_file)


test = VirusradarParser()
