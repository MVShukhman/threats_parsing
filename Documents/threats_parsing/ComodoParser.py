from base import Base
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import requests


class ComodoParser(Base):
    _identifier = 'comodo'
    _base_url = 'https://knowledge-base.threatlabs.comodo.com/'

    def _get_links(self, url) -> list:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('ignore-certificate-errors')
        chrome_driver_path = os.getcwd() + '/Drivers/chromedriver'
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver_path)
        driver.get('https://knowledge-base.threatlabs.comodo.com/')
        driver.implicitly_wait(4)
        button = driver.find_element_by_css_selector("#s2id_formInput > a > span.select2-arrow")
        button.click()
        code = driver.page_source
        driver.quit()
        soup = bs(code, 'html.parser')
        items = soup.find_all('li', {'class': 'select2-results-dept-0 select2-result select2-result-selectable'})
        links = []
        for x in items:
            s = x.div.text
            name = s.replace(' ', '%20')
            links.append('https://knowledge-base.threatlabs.comodo.com/family/{}'.format(s))

        self.n = len(links)
        self.cnt = 1

        return links

    def _parse_by_link(self, url) -> dict:
        resp = requests.get(url, verify=False)
        code = resp.content
        soup = bs(code, 'html.parser')

        block = soup.find('div', {'class': 'col-md-9 text-block'})
        name = block.h1.text

        ans = {
            'name': name,
            'url': url,
            'source_keyword': self._identifier,
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

        print('{}/{}'.format(self.cnt, self.n))
        self.cnt += 1

        return ans


test = ComodoParser()
test.run_parsing()
