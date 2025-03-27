import pytest
from portman_testing.helpers.test_config import PortmanTestEnvironment
from portman_testing.db.mock_postgres import MockPostgresDB

# In tests/conftest.py, add:
collect_ignore = [
    "../src/portman_testing/helpers/test_config.py",
    "../src/portman_testing/helpers/config.py"
]

def pytest_addoption(parser):
    """Add command-line options to pytest."""
    parser.addoption(
        "--env",
        action="store",
        default="test",
        help="Test environment to use: test, dev, or prod"
    )
    parser.addoption(
        "--db-host",
        action="store",
        help="Database host"
    )
    parser.addoption(
        "--db-port",
        action="store",
        help="Database port"
    )
    parser.addoption(
        "--db-name",
        action="store",
        help="Database name"
    )
    parser.addoption(
        "--db-user",
        action="store",
        help="Database user"
    )
    parser.addoption(
        "--db-password",
        action="store",
        help="Database password"
    )
    parser.addoption(
        "--api-url",
        action="store",
        help="API URL"
    )


@pytest.fixture(scope="session")
def test_config(request):
    """Create test configuration based on command-line options."""
    # Get environment from command line
    env_name = request.config.getoption("--env")

    # Create base configuration
    config = PortmanTestEnvironment(env_name)

    # Override with command-line options if provided
    for option in ["db_host", "db_port", "db_name", "db_user", "db_password", "api_url"]:
        cmd_option = option.replace("_", "-")
        value = request.config.getoption(f"--{cmd_option}")
        if value is not None:
            config.config[option] = value

    return config


@pytest.fixture(scope="session")
def db(test_config):
    """Create database connection using test configuration."""
    db = MockPostgresDB(
        dbname=test_config.get("db_name"),
        user=test_config.get("db_user"),
        password=test_config.get("db_password"),
        host=test_config.get("db_host"),
        port=test_config.get("db_port")
    )

    # Set up test database
    test_db_name = db.setup_test_db()

    yield db

    # Clean up
    db.teardown_test_db()
