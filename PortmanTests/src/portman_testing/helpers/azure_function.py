"""
Azure Function helper utilities for testing.

This module provides helper functions and classes for testing
Azure Functions in the Portman Agent.
"""

import json
import uuid
from typing import Dict, List, Any, Optional, Union, Callable
from datetime import datetime


class MockHttpTrigger:
    """
    Mock implementation of Azure Function HTTP trigger.

    This class simulates the behavior of an HTTP trigger for testing
    Azure Functions without deploying them.
    """

    def __init__(self,
                 method: str = "GET",
                 route: Optional[str] = None,
                 params: Optional[Dict[str, str]] = None,
                 headers: Optional[Dict[str, str]] = None,
                 body: Optional[Union[Dict[str, Any], str]] = None):
        """
        Initialize the MockHttpTrigger instance.

        Args:
            method: HTTP method (default: "GET")
            route: Function route (default: None)
            params: Query parameters (default: None)
            headers: HTTP headers (default: None)
            body: Request body (default: None)
        """
        self.method = method
        self.route = route
        self.params = params or {}
        self.headers = headers or {
            "Content-Type": "application/json"
        }
        self.body = body
        self.url = f"https://example.com/api/{route}" if route else "https://example.com/api"

    def get_json(self) -> Dict[str, Any]:
        """
        Get the request body as JSON.

        Returns:
            Dictionary containing the request body
        """
        if isinstance(self.body, dict):
            return self.body
        elif isinstance(self.body, str):
            try:
                return json.loads(self.body)
            except json.JSONDecodeError:
                return {}
        else:
            return {}

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the HTTP trigger to a dictionary.

        Returns:
            Dictionary representation of the HTTP trigger
        """
        return {
            "method": self.method,
            "url": self.url,
            "headers": self.headers,
            "params": self.params,
            "body": self.body
        }


class MockContext:
    """
    Mock implementation of Azure Function execution context.

    This class simulates the behavior of an Azure Function execution context
    for testing functions without deploying them.
    """

    def __init__(self,
                 function_name: str = "PortmanFunction",
                 function_directory: str = "/home/site/wwwroot",
                 invocation_id: Optional[str] = None):
        """
        Initialize the MockContext instance.

        Args:
            function_name: Name of the function (default: "PortmanFunction")
            function_directory: Directory of the function (default: "/home/site/wwwroot")
            invocation_id: Unique invocation ID (default: None, auto-generated)
        """
        self.function_name = function_name
        self.function_directory = function_directory
        self.invocation_id = invocation_id or str(uuid.uuid4())
        self.logs = []

    def log(self, message: str) -> None:
        """
        Log a message.

        Args:
            message: Message to log
        """
        timestamp = datetime.now().isoformat()
        self.logs.append(f"[{timestamp}] {message}")

    def get_logs(self) -> List[str]:
        """
        Get all logged messages.

        Returns:
            List of logged messages
        """
        return self.logs


def mock_context(function_name: str = "PortmanFunction") -> MockContext:
    """
    Create a mock execution context.

    Args:
        function_name: Name of the function (default: "PortmanFunction")

    Returns:
        MockContext instance
    """
    return MockContext(function_name=function_name)


def mock_http_trigger(method: str = "GET",
                      params: Optional[Dict[str, str]] = None,
                      body: Optional[Union[Dict[str, Any], str]] = None) -> MockHttpTrigger:
    """
    Create a mock HTTP trigger.

    Args:
        method: HTTP method (default: "GET")
        params: Query parameters (default: None)
        body: Request body (default: None)

    Returns:
        MockHttpTrigger instance
    """
    return MockHttpTrigger(method=method, params=params, body=body)


def simulate_function_call(func: Callable,
                           req: Optional[MockHttpTrigger] = None,
                           context: Optional[MockContext] = None) -> Any:
    """
    Simulate an Azure Function call.

    Args:
        func: Function to call
        req: HTTP trigger (default: None, creates a default GET request)
        context: Execution context (default: None, creates a default context)

    Returns:
        Function result
    """
    if req is None:
        req = mock_http_trigger()

    if context is None:
        context = mock_context()

    return func(req, context)
