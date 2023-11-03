import os
import unittest
from get_settings_yaml import parse_settings


TEST_PATH = os.path.dirname(__file__)


class TestParseSettings(unittest.TestCase):

    def test_load_test_settings(self):
        settings = parse_settings(base_path=TEST_PATH,
                                  settings_filename='test_settings.yaml')
        assert isinstance(settings, dict)
        for _k, _v in settings.items():
            assert _v.startswith('test')

    def test_load_top_level_settings(self):
        settings = parse_settings()
        assert isinstance(settings, dict)
        assert settings == {'key': 123, 'passcode': 'abc'}

    def test_load_top_level_settings_from_tests(self):
        settings = parse_settings(base_path=TEST_PATH)
        assert isinstance(settings, dict)
        assert settings == {'key': 123, 'passcode': 'abc'}
