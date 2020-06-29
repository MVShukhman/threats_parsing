import os
import json


class Base:  # Abstract class for parsers
    _header = {
        'User-Agent': ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) '
                       'Gecko/20100101 Firefox/50.0')
    }

    def __init__(self):
        self.__links_filepath = 'Data/Links/{}_links.json'.format(self._identifier)
        self.__data_filepath = 'Data/Descriptions/{}_data.json'.format(self._identifier)
        if not os.path.exists(self.__links_filepath) or os.stat(self.__links_filepath).st_size == 0:
            self.__save_links_to_file()
        with open(self.__links_filepath, 'r') as json_file:
            self.__links = json.load(json_file)

    def _get_links(self, url) -> list:  # The main methods for implementing in parsers
        pass

    def _parse_by_link(self, url) -> dict:
        pass

    def __save_links_to_file(self):
        links = self._get_links(self._base_url)
        with open(self.__links_filepath, 'w') as json_file:
            json.dump(links, json_file)

    def run_parsing(self):
        with open(self.__data_filepath, 'w') as json_file:
            json.dump([self._parse_by_link(url) for url in self.__links], json_file)
