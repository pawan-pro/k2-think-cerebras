import unittest
from unittest.mock import patch, AsyncMock
from src.cli.api import get_client

class TestApi(unittest.IsolatedAsyncioTestCase):

    @patch("src.cli.api.get_api_key", return_value="test_api_key")
    @patch("src.cli.api.AsyncCerebras")
    async def test_get_client(self, mock_cerebras_client, mock_get_api_key):
        # Mock the AsyncCerebras client
        mock_client_instance = AsyncMock()
        mock_cerebras_client.return_value = mock_client_instance

        # Call the function
        client = await get_client()

        # Assertions
        mock_get_api_key.assert_called_once()
        mock_cerebras_client.assert_called_once_with(api_key="test_api_key")
        self.assertEqual(client, mock_client_instance)

    @patch("src.cli.api.get_api_key", return_value=None)
    async def test_get_client_no_key(self, mock_get_api_key):
        with self.assertRaises(ValueError):
            await get_client()

if __name__ == "__main__":
    unittest.main()