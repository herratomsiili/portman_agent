"""
API mocking module for Digitraffic port call API.

This module provides tools to mock the Digitraffic port call API responses
for testing the Portman Agent without making actual API calls.
"""

import json
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Any

from .response_templates import (
    get_port_call_template,
    get_error_response,
    get_empty_response
)


class MockDigitraffic:
    """
    Mock implementation of the Digitraffic port call API.

    This class simulates the behavior of the Digitraffic API for testing purposes,
    allowing developers to test the Portman Agent without making actual API calls.
    """

    def __init__(self, base_url: str = "https://meri.digitraffic.fi/api/port-call/v1"):
        """
        Initialize the MockDigitraffic instance.

        Args:
            base_url: The base URL of the Digitraffic API (default: "https://meri.digitraffic.fi/api/port-call/v1")
        """
        self.base_url = base_url
        self.should_timeout = False
        self.should_error = False
        self.error_code = 500
        self.error_message = "Internal Server Error"
        self.delay_seconds = 0

    def configure(self,
                  timeout: bool = False,
                  error: bool = False,
                  error_code: int = 500,
                  error_message: str = "Internal Server Error",
                  delay_seconds: float = 0) -> None:
        """
        Configure the behavior of the mock API.

        Args:
            timeout: Whether the API should simulate a timeout
            error: Whether the API should return an error response
            error_code: HTTP error code to return if error is True
            error_message: Error message to include in the response if error is True
            delay_seconds: Number of seconds to delay the response
        """
        self.should_timeout = timeout
        self.should_error = error
        self.error_code = error_code
        self.error_message = error_message
        self.delay_seconds = delay_seconds

    def mock_port_calls(self,
                        imo_numbers: Optional[List[str]] = None,
                        count: int = 5,
                        from_date: Optional[str] = None,
                        to_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate mock port call data for the specified IMO numbers.

        Args:
            imo_numbers: List of IMO numbers to include in the response
            count: Number of port calls to generate per IMO number
            from_date: Start date for port calls (ISO format)
            to_date: End date for port calls (ISO format)

        Returns:
            Dict containing mock port call data in the same format as the Digitraffic API
        """
        # Simulate network delay
        if self.delay_seconds > 0:
            time.sleep(self.delay_seconds)

        # Simulate timeout
        if self.should_timeout:
            raise TimeoutError("Connection timed out")

        # Simulate error response
        if self.should_error:
            return get_error_response(self.error_code, self.error_message)

        # If no IMO numbers provided, return empty response
        if not imo_numbers or len(imo_numbers) == 0:
            return get_empty_response()

        # Generate mock port calls for each IMO number
        port_calls = []

        # Set date range if not provided
        if not from_date:
            from_date_obj = datetime.now() - timedelta(days=30)
        else:
            from_date_obj = datetime.fromisoformat(from_date.replace('Z', '+00:00'))

        if not to_date:
            to_date_obj = datetime.now() + timedelta(days=30)
        else:
            to_date_obj = datetime.fromisoformat(to_date.replace('Z', '+00:00'))

        # Generate port calls for each IMO number
        for imo in imo_numbers:
            for _ in range(count):
                # Generate a random date within the range
                days_range = (to_date_obj - from_date_obj).days
                random_days = random.randint(0, days_range)
                event_date = from_date_obj + timedelta(days=random_days)

                # Create a port call using the template
                port_call = get_port_call_template(
                    imo=imo,
                    event_timestamp=event_date.isoformat() + 'Z'
                )
                port_calls.append(port_call)

        # Sort port calls by timestamp
        port_calls.sort(key=lambda x: x.get('portCallTimestamp', ''))

        # Return the response in the same format as the Digitraffic API
        return {
            "portCalls": port_calls,
            "metadata": {
                "resultCount": len(port_calls),
                "from": from_date_obj.isoformat() + 'Z',
                "to": to_date_obj.isoformat() + 'Z'
            }
        }

    def simulate_error(self, error_code: int = 500, error_message: str = "Internal Server Error") -> Dict[str, Any]:
        """
        Simulate an API error response.

        Args:
            error_code: HTTP error code to return
            error_message: Error message to include in the response

        Returns:
            Dict containing error response
        """
        return get_error_response(error_code, error_message)

    def simulate_timeout(self) -> None:
        """
        Simulate a connection timeout.

        Raises:
            TimeoutError: Always raises this exception to simulate a timeout
        """
        raise TimeoutError("Connection timed out")
