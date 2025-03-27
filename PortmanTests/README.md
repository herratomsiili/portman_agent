# Portman Testing Package

A testing package for the Portman Agent that provides tools for:
- Mocking the Digitraffic port call API
- Testing database operations
- Creating test fixtures for vessel data
- Helper utilities for Azure Function testing

## Installation

```bash
cd PortmanTests

# Install the package in development mode
pip install -e .

# Or install directly from the repository
pip install git+https://github.com/your-organization/portman-testing.git
```

## Features

- **API Mocking**: Mock the Digitraffic port call API to test without making actual API calls
- **Database Testing**: Create temporary test databases with the Portman Agent schema
- **Test Fixtures**: Generate vessel and port call data for testing
- **Azure Function Helpers**: Simulate HTTP triggers and execution contexts
- **Configuration Utilities**: Manage test configurations and environment variables

## Requirements

- Python 3.8 or higher
- PostgreSQL 12 or higher
- psycopg2
