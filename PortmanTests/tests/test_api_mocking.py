"""
Example test case for API mocking functionality.

This module demonstrates how to use the API mocking functionality
of the Portman testing package.
"""

import unittest
from datetime import datetime, timedelta

from portman_testing.api.mock_digitraffic import MockDigitraffic


class TestApiMocking(unittest.TestCase):
    """Test cases for API mocking functionality."""

    def setUp(self):
        """Set up test environment."""
        self.mock_api = MockDigitraffic()
        self.test_imo_numbers = ["9123456", "9234567", "9345678"]

    def test_mock_port_calls_basic(self):
        """Test basic port call mocking."""
        # Get mock port calls for test IMO numbers
        response = self.mock_api.mock_port_calls(
            imo_numbers=self.test_imo_numbers,
            count=2
        )

        # Verify response structure
        self.assertIn("portCalls", response)
        self.assertIn("metadata", response)

        # Verify port calls count (2 per IMO number)
        self.assertEqual(len(response["portCalls"]), 6)
        self.assertEqual(response["metadata"]["resultCount"], 6)

        # Verify port calls contain expected IMO numbers
        imo_numbers_in_response = set()
        for port_call in response["portCalls"]:
            self.assertIn("vessel", port_call)
            self.assertIn("imo", port_call["vessel"])
            imo_numbers_in_response.add(port_call["vessel"]["imo"])

        self.assertEqual(imo_numbers_in_response, set(self.test_imo_numbers))

    def test_mock_port_calls_date_range(self):
        """Test port call mocking with date range."""
        # Define date range
        from_date_obj = datetime.now().replace(tzinfo=None) - timedelta(days=10)
        to_date_obj = datetime.now().replace(tzinfo=None)

        # Format date range
        from_date = from_date_obj.replace(microsecond=0).isoformat()
        to_date = to_date_obj.replace(microsecond=0).isoformat()

        # Get mock port calls with date range
        response = self.mock_api.mock_port_calls(
            imo_numbers=self.test_imo_numbers,
            count=1,
            from_date=from_date,
            to_date=to_date
        )
        testi = response["metadata"]["from"]
        print("\n#####\n####testi: ", testi, "\n#####")
        from_date = from_date + 'Z'
        to_date = to_date + 'Z'

        # Verify metadata contains correct date range
        self.assertEqual(response["metadata"]["from"], from_date)
        self.assertEqual(response["metadata"]["to"], to_date)

    def testi1(self):
        """testi1 jee!!!"""
        self.assertEqual(1, 1)

    def test_empty_response(self):
        """Test empty response when no IMO numbers provided."""
        response = self.mock_api.mock_port_calls(imo_numbers=[])

        # Verify empty response
        self.assertEqual(len(response["portCalls"]), 0)
        self.assertEqual(response["metadata"]["resultCount"], 0)

    def test_error_simulation(self):
        """Test error simulation."""
        # Configure API to return an error
        self.mock_api.configure(error=True, error_code=404, error_message="Not Found")

        # Get mock port calls
        response = self.mock_api.mock_port_calls(imo_numbers=self.test_imo_numbers)

        # Verify error response
        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], 404)
        self.assertEqual(response["error"]["message"], "Not Found")

    def test_timeout_simulation(self):
        """Test timeout simulation."""
        # Configure API to timeout
        self.mock_api.configure(timeout=True)

        # Verify timeout exception is raised
        with self.assertRaises(TimeoutError):
            self.mock_api.mock_port_calls(imo_numbers=self.test_imo_numbers)

    def test_delay_simulation(self):
        """Test delay simulation."""
        # Configure API with a small delay
        self.mock_api.configure(delay_seconds=0.1)

        # Measure response time
        start_time = datetime.now()
        self.mock_api.mock_port_calls(imo_numbers=self.test_imo_numbers)
        end_time = datetime.now()

        # Verify delay
        elapsed_seconds = (end_time - start_time).total_seconds()
        self.assertGreaterEqual(elapsed_seconds, 0.1)


if __name__ == "__main__":
    unittest.main()
