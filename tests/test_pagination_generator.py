import unittest
from unittest.mock import MagicMock
from keka.utils.pagination import PaginatedCursor


def _make_mock_client(total_pages=3):
    """Create a mock client that returns paginated responses."""
    client = MagicMock()

    def mock_get(endpoint, params=None, headers=None):
        params = params or {}
        page = int(params.get('pageNumber', 1))

        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {
            "succeeded": True,
            "message": f"Page {page} of {total_pages}",
            "errors": [],
            "data": [f"item_page{page}"],
            "pageNumber": page,
            "pageSize": 10,
            "totalPages": total_pages,
            "totalRecords": total_pages * 10,
            "nextPage": f"http://api/next?pageNumber={page + 1}" if page < total_pages else None,
        }
        return response

    client.get.side_effect = mock_get
    return client


class TestPaginationGenerator(unittest.TestCase):
    """Tests for the self-referencing generator pagination pattern."""

    def test_pagination_three_pages(self):
        """Iterate through 3 pages using the self-referencing next_page generator."""
        client = _make_mock_client(total_pages=3)

        result = PaginatedCursor.execute(client, "/test")

        # Page 1 — returned directly by execute()
        self.assertTrue(result["succeeded"])
        self.assertEqual(result["data"], ["item_page1"])
        self.assertIsNotNone(result["next_page"])

        # Page 2 — obtained via next() on the generator
        page2 = next(result["next_page"])
        self.assertTrue(page2["succeeded"])
        self.assertEqual(page2["data"], ["item_page2"])
        self.assertIsNotNone(page2["next_page"])

        # Page 3 — obtained via next() on page2's generator
        page3 = next(page2["next_page"])
        self.assertTrue(page3["succeeded"])
        self.assertEqual(page3["data"], ["item_page3"])
        self.assertIsNone(page3["next_page"])  # Last page → None

    def test_stop_iteration_after_last_page(self):
        """StopIteration is raised when calling next() after all pages consumed."""
        client = _make_mock_client(total_pages=2)

        result = PaginatedCursor.execute(client, "/test")
        gen = result["next_page"]

        # Page 2 (last page)
        page2 = next(gen)
        self.assertEqual(page2["data"], ["item_page2"])
        self.assertIsNone(page2["next_page"])

        # No more pages → StopIteration
        with self.assertRaises(StopIteration):
            next(gen)

    def test_single_page_response(self):
        """When totalPages == 1, next_page should be None directly from execute()."""
        client = _make_mock_client(total_pages=1)

        result = PaginatedCursor.execute(client, "/test")
        self.assertEqual(result["data"], ["item_page1"])
        self.assertIsNone(result["next_page"])

    def test_filters_preserved_across_pages(self):
        """Original query parameters (filters, sorting) are preserved in every request."""
        client = _make_mock_client(total_pages=3)
        original_params = {
            "status": "active",
            "departmentId": "dept-123",
            "pageSize": 25,
            "sort": "name:asc",
        }

        result = PaginatedCursor.execute(client, "/api/v1/employees", params=original_params)

        # Consume all pages via generators
        page2 = next(result["next_page"])
        page3 = next(page2["next_page"])

        # Verify every call preserved the original params
        for call_args in client.get.call_args_list:
            actual_params = call_args.kwargs.get("params") or call_args[1].get("params", {})
            self.assertEqual(actual_params.get("status"), "active")
            self.assertEqual(actual_params.get("departmentId"), "dept-123")
            self.assertEqual(actual_params.get("pageSize"), 25)
            self.assertEqual(actual_params.get("sort"), "name:asc")

    def test_no_extra_api_calls_after_last_page(self):
        """After the last page, no additional API requests should be made."""
        client = _make_mock_client(total_pages=2)

        result = PaginatedCursor.execute(client, "/test")
        page2 = next(result["next_page"])

        call_count_after_last = client.get.call_count

        # Attempting next() after exhaustion should NOT make another API call
        with self.assertRaises(StopIteration):
            next(result["next_page"])

        self.assertEqual(client.get.call_count, call_count_after_last)

    def test_failed_initial_request(self):
        """When the initial request fails, next_page should be None."""
        client = MagicMock()
        response = MagicMock()
        response.status_code = 500
        client.get.return_value = response

        result = PaginatedCursor.execute(client, "/test")
        self.assertIsNone(result["next_page"])
        self.assertEqual(result["data"], [])

    def test_failed_intermediate_page(self):
        """If a page fetch fails mid-pagination, the generator terminates gracefully."""
        client = MagicMock()
        call_count = 0

        def mock_get(endpoint, params=None, headers=None):
            nonlocal call_count
            call_count += 1
            response = MagicMock()

            if call_count == 1:
                # Initial request succeeds
                response.status_code = 200
                response.json.return_value = {
                    "succeeded": True,
                    "data": ["page1"],
                    "pageNumber": 1,
                    "totalPages": 3,
                }
            else:
                # Subsequent request fails
                response.status_code = 500

            return response

        client.get.side_effect = mock_get

        result = PaginatedCursor.execute(client, "/test")
        self.assertIsNotNone(result["next_page"])

        # Attempting to get page 2 should stop iteration (server error)
        with self.assertRaises(StopIteration):
            next(result["next_page"])


if __name__ == '__main__':
    unittest.main()
