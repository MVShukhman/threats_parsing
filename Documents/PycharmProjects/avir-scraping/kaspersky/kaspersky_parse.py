from bs4 import BeautifulSoup
import json
import requests


class KasperskyParser:
    link = 'https://threats.kaspersky.com/en/wp-admin/admin-ajax.php'
    user_agent = ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) '
                  'Gecko/20100101 Firefox/50.0')
    links = []
    storage = []
    payload = {
        'action': 'infinite_scroll',
        'page_no': '32',
        'post_type': 'threat',
        'template': 'row_threat4archive',
        's_post_type': 'threat',
        'orderby': 'detect_date',
        'meta_key': 'true',
        'order': 'desc'
    }

    def __init__(self):
        pass
        #self.get_links()

    def get_links(self):
        for i in range(1, 49):
            self.payload['page_no'] = str(i)
            resp = requests.post(url=self.link, data=self.payload)
            code = resp.content.decode('utf-8')
            soup = BeautifulSoup(code, 'html.parser')
            threats = soup.find_all('tr', {'class': 'line_info line_info_threat'})
            for x in threats:
                self.links.append(x.find('a')['href'])

        with open('kaspersky_links.json', 'w') as json_file:
            json.dump(self.links, json_file)

    def fill_storage(self):
        with open('kaspersky_links.json', 'r') as json_file:
            self.links = json.load(json_file)
        for i, link in enumerate(self.links):
            threat = {'link': link}
            resp = requests.get(link)
            code = resp.content
            soup = BeautifulSoup(code, 'html.parser')
            table = soup.find('table', {'class': 'table_informations table_informations_ugrozy'})
            blocks = table.find_all('tr', {'class': 'line_info'})
            for block in blocks:
                key = block.find('td', {'class': 'cell_one cell_one_icone'})
                if key is None:
                    continue
                info = block.find('td', {'class': 'cell_two'})
                if key.text == 'Description':
                    threat[key.text] = info.find('p').text
                else:
                    threat[key.text] = info.text

            self.storage.append(threat)
            print(i + 1, '/', len(self.links))

    def save_data(self):
        with open('kaspersky_data.json', 'w') as json_file:
            json.dump(self.storage, json_file)
        print('DONE!')


test = KasperskyParser()

test.fill_storage()
test.save_data()
