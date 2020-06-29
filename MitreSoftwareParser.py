from base import Base
from bs4 import BeautifulSoup as bs
import requests


class MitreSoftwareParser(Base):
    _identifier = 'mitre-software'
    _base_url = 'https://attack.mitre.org/software/'

    def _get_links(self, url) -> list:
        resp = requests.get(url)
        code = resp.content
        soup = bs(code, 'html.parser')
        table = soup.find('table', {'class': 'table table-bordered table-alternate mt-2'}).tbody
        rows = table.find_all('tr')
        links = []
        for row in rows:
            curr = row.find('td')
            tail = curr.a['href']
            links.append('{}{}'.format(url, tail[10:]))
        self.n = len(links)
        self.count = 1
        return links

    def _parse_by_link(self, url) -> dict:
        resp = requests.get(url)
        code = resp.content
        soup = bs(code, 'html.parser')
        table = soup.find('div', {'class': 'jumbotron jumbotron-fluid'})
        table = table.find('div', {'class': 'container-fluid'})
        name = table.h1.text.strip()
        ans = {
            'name': name,
            'url': url,
            'source_keyword': self._identifier,
            'info': {}
        }

        table = table.find('div', {'class': 'row'})
        description_block = table.find('div', {'class': 'col-md-8 description-body'})
        ans['info']['decription'] = description_block.text
        overview_block = table.find('div', {'class': 'col-md-4'})
        items = overview_block.find_all('div', {'class': 'card-data'})
        for item in items:
            txt = item.text
            pos = txt.find(':')
            key = txt[:pos].strip()
            value = txt[pos + 1:].strip()
            ans['info'][key] = value

        print('{}/{}'.format(self.count, self.n))
        self.count += 1

        return ans


test = MitreSoftwareParser()
test.run_parsing()
