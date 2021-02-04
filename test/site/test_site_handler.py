import unittest
from unittest.mock import MagicMock, patch

from updater.site import site_handler
from updater.site.curse import Curse
from updater.site.enum import AddonVersion, GameVersion
from updater.site.tukui import Tukui
from updater.site.wowace import WoWAce
from updater.site.wowinterface import WoWInterface
from updater.site.townlongyak import Townlongyak


class TestSiteHandler(unittest.TestCase):
    @patch.object(Curse, '_normalize_curse_urls', MagicMock(return_value=''))
    def test_handles_curse(self):
        for url in Curse.get_supported_urls():
            handler = site_handler.get_handler(url, GameVersion.retail)
            self.assertIsInstance(handler, Curse)

    @patch.object(Curse, '_normalize_curse_urls', MagicMock(return_value=''))
    def test_handles_curse_prerelease(self):
        addon_versions = AddonVersion.__members__.values()
        for url in Curse.get_supported_urls():
            for version in addon_versions:
                handler = site_handler.get_handler(url, GameVersion.retail, version)
                self.assertEqual(handler.addon_version, version)

    def test_handles_wowace(self):
        for url in WoWAce.get_supported_urls():
            handler = site_handler.get_handler(url, GameVersion.retail)
            self.assertIsInstance(handler, WoWAce)

    def test_handles_tukui(self):
        for url in WoWInterface.get_supported_urls():
            handler = site_handler.get_handler(url, GameVersion.retail)
            self.assertIsInstance(handler, WoWInterface)

    def test_handles_wowinterface(self):
        for url in Tukui.get_supported_urls():
            handler = site_handler.get_handler(url, GameVersion.retail)
            self.assertIsInstance(handler, Tukui)

    def test_handles_townlongyak(self):
        for url in Townlongyak.get_supported_urls():
            handler = site_handler.get_handler(url, GameVersion.retail)
            self.assertIsInstance(handler, Townlongyak)


if __name__ == '__main__':
    unittest.main()
