import os
import unittest
from get_settings_yaml import load_path


TEST_PATH = os.path.dirname(__file__)


class TestLoadSettings(unittest.TestCase):

    def test_load_test_settings(self):
        settings = load_path(base_path=TEST_PATH,
                             settings_filename='test_settings.yaml')
        assert isinstance(settings, str)
        assert settings.endswith('/get-settings-yaml/tests/test_settings.yaml')

    def test_load_top_level_settings(self):
        settings = load_path()
        assert isinstance(settings, str)
        assert settings.endswith('/get-settings-yaml/settings.yaml')

    def test_load_top_level_settings_from_tests(self):
        settings = load_path(base_path=TEST_PATH)
        assert isinstance(settings, str)
        assert settings.endswith('/get-settings-yaml/settings.yaml')
