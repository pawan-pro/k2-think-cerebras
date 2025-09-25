import unittest
from unittest.mock import mock_open, patch
from src.cli.config import load_config, get_api_key

class TestConfig(unittest.TestCase):

    @patch("src.cli.config.Path.is_file", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data="api_key: test_key\nmodel: test_model")
    def test_load_config(self, mock_file, mock_is_file):
        config = load_config()
        self.assertEqual(config, {"api_key": "test_key", "model": "test_model"})

    @patch("src.cli.config.load_config", return_value={"api_key": "test_key"})
    def test_get_api_key(self, mock_load_config):
        api_key = get_api_key()
        self.assertEqual(api_key, "test_key")

if __name__ == "__main__":
    unittest.main()