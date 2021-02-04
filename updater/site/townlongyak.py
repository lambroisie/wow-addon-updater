import re

import requests
from bs4 import BeautifulSoup

from updater.site.abstract_site import AbstractSite
from updater.site.enum import GameVersion


class Townlongyak(AbstractSite):
    _URLS = [
        'https://www.townlong-yak.com/'
    ]

    session = requests.session()

    latest_version = None

    _page: BeautifulSoup = None

    _version_pattern = r'(?P<version>[\d]+\.[\d]+)'

    def __init__(self, url: str):
        super().__init__(url, GameVersion.agnostic)

    def find_zip_url(self):
        # For classic or retail misc addons:
        # https://www.tukui.org/classic-addons.php?id=1
        # or https://www.tukui.org/addons.php?id=3
        # becomes
        # https://www.tukui.org/classic-addons.php?download=1
        # and https://www.tukui.org/addons.php?id=3
        #
        # Or for retail ONLY elvui and tukui themselves:
        # https://www.tukui.org/download.php?ui=tukui
        # https://www.tukui.org/download.php?ui=elvui
        # becomes
        # https://www.tukui.org/downloads/elvui-11.372.zip

        download_link = self._get_page().find('a', attrs={'class': 'c-link cm'})['href']
        download_link = Townlongyak._URLS[0] + download_link[1:]  # take off the leading / from the href
        return download_link

    def get_latest_version(self):
            version = re.search(self._version_pattern, self.find_zip_url()).group(1)
            self.latest_version = version
            return version

    def get_addon_name(self):
        if self._is_special_tukui_link():
            # wow I hate this so much, but it works
            return "VenturePlan"
        else:
            name = self._get_page().find('span', attrs={'class': 'Member'})
            addon_name = name.text.strip()
        return addon_name

    def _is_special_tukui_link(self):
        return any([self.url.endswith(ending) for ending in ['venture-plan']])

    def _get_page(self):
        try:
            if not self._page:
                response = Townlongyak.session.get(self.url)
                response.raise_for_status()
                self._page = BeautifulSoup(response.text, 'html.parser')
            return self._page
        except Exception as e:
            raise self.download_error() from e
