from unittest import TestCase
from unittest.mock import patch, Mock
from src.unglue_it_driver.retrieve import (
    get_path,
    fetch_results,
)

from src.unglue_it_driver.serializers import UnglueReportItem

class MockUnglueReportItem:
    """Mock the UnglueReportItem object from the serializer."""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class TestRetrieve(TestCase):
    def setUp(self) -> None:
        return

    @patch("src.unglue_it_driver.retrieve.httplib2.Http")
    def test_get_path_valid_url(self, mock_http: Mock) -> None:
        url = "your_valid_url_here"
        mock_response = Mock()
        mock_response.status = 200
        mock_response.data = b'{"some_key": "some_value"}'
        mock_http.return_value.request.return_value = (
            mock_response,
            mock_response.data,
        )

        result = get_path(url)

        self.assertIsInstance(result, dict)
        self.assertEqual(result, {"some_key": "some_value"})

    @patch("src.unglue_it_driver.retrieve.httplib2.Http")
    def test_get_path_invalid_url(self, mock_http: Mock) -> None:
        url = "your_invalid_url_here"
        mock_response = Mock()
        mock_response.status = 404
        mock_response.data = b"Not Found"
        mock_http.return_value.request.return_value = (
            mock_response,
            mock_response.data,
        )

        with self.assertLogs() as logs:
            result = get_path(url)

        # Assert that response.raise_for_status() was called
        mock_response.raise_for_status.assert_called_once()

    @patch("src.unglue_it_driver.retrieve.get_path")
    @patch("src.unglue_it_driver.retrieve.get_api_url")
    def test_fetch_results_and_count_them(self, mock_get_api_url, mock_get_path):
        """Demonstrate the fetch results work and count the results."""
        path_url = (
            "https://unglue.it/test?format=json&api_key=test_key&username=test_user"
        )
        ebook_path_url = "your_valid_ebook_url_here"
        edition_url = "your_valid_edition_url_here"

        # Mock the behavior of get_api_url
        mock_get_api_url.side_effect = [path_url, ebook_path_url, edition_url]

        # Mock the response data for get_path
        publisher_and_path = {"ebooks": ["ebook1", "ebook2"]}
        book_results = {"edition": "edtion_test"}
        book_results = {
            "edition": "edition_test",
            "download_count": 5,
            "resource_uri": "test_resource",
            "identifiers": [
                {
                    "edition": "/test/edition/1",
                    "id": 12345,
                    "type": "goog",
                    "value": "ABC12345",
                    "work": "/api/v1/work/12345/",
                },
                {
                    "edition": "/test/edition/2",
                    "id": 123456,
                    "type": "isbn",
                    "value": "123456789",
                    "work": "/api/v1/work/12345/",
                },
            ],
        }

        mock_get_path.side_effect = [publisher_and_path, book_results, book_results]
        results = fetch_results('test_api_key', 1, 'test@test.com')

        for result in results:
            self.assertIsInstance(result, UnglueReportItem)
            yield f"{result.downloads}{result.resource_uri}{result.instances}"
