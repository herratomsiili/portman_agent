"""
Configuration utilities for testing.

This module provides utilities for managing test configurations
and environment variables for the Portman Agent.
"""

import os
import json
from typing import Dict, Any, Optional, Union
from pathlib import Path


class PortmanConfig:
    """
    Configuration manager for testing.

    This class provides methods for loading, saving, and managing
    test configurations for the Portman Agent.
    """

    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize the TestConfig instance.

        Args:
            config_file: Path to configuration file (default: None)
        """
        self.config_file = config_file
        self.config = {}

        # Load configuration if file is provided
        if config_file:
            self.load_config()

    def load_config(self, config_file: Optional[str] = None) -> Dict[str, Any]:
        """
        Load configuration from file.

        Args:
            config_file: Path to configuration file (default: None, uses self.config_file)

        Returns:
            Dictionary containing configuration
        """
        file_path = config_file or self.config_file

        if not file_path:
            return {}

        try:
            with open(file_path, 'r') as f:
                self.config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.config = {}

        return self.config

    def save_config(self, config_file: Optional[str] = None) -> None:
        """
        Save configuration to file.

        Args:
            config_file: Path to configuration file (default: None, uses self.config_file)
        """
        file_path = config_file or self.config_file

        if not file_path:
            return

        # Create directory if it doesn't exist
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        with open(file_path, 'w') as f:
            json.dump(self.config, f, indent=2)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.

        Args:
            key: Configuration key
            default: Default value if key doesn't exist

        Returns:
            Configuration value
        """
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value.

        Args:
            key: Configuration key
            value: Configuration value
        """
        self.config[key] = value

    def update(self, config: Dict[str, Any]) -> None:
        """
        Update configuration with dictionary.

        Args:
            config: Dictionary containing configuration values
        """
        self.config.update(config)


def get_env_var(name: str, default: Any = None) -> str:
    """
    Get environment variable.

    Args:
        name: Environment variable name
        default: Default value if environment variable doesn't exist

    Returns:
        Environment variable value
    """
    return os.environ.get(name, default)


def set_env_var(name: str, value: str) -> None:
    """
    Set environment variable.

    Args:
        name: Environment variable name
        value: Environment variable value
    """
    os.environ[name] = value


def load_env_file(env_file: str) -> Dict[str, str]:
    """
    Load environment variables from .env file.

    Args:
        env_file: Path to .env file

    Returns:
        Dictionary containing environment variables
    """
    env_vars = {}

    try:
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()

                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue

                # Parse key-value pairs
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()

                    # Remove quotes if present
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]

                    env_vars[key] = value
                    set_env_var(key, value)
    except FileNotFoundError:
        pass

    return env_vars


def get_test_config(environment: str = "test") -> Dict[str, Any]:
    """
    Get configuration for specific test environment.

    Args:
        environment: Environment name (default: "test")

    Returns:
        Dictionary containing configuration for the environment
    """
    # Default configurations for different environments
    configs = {
        "test": {
            "api_url": "https://meri.digitraffic.fi/api/port-call/v1",
            "db_host": "localhost",
            "db_port": "5432",
            "db_name": "portman",
            "db_user": "postgres",
            "db_password": "postgres",
            "function_auth_code": "test_code",
            "log_level": "DEBUG"
        },
        "development": {
            "api_url": "https://meri.digitraffic.fi/api/port-call/v1",
            "db_host": "localhost",
            "db_port": "5432",
            "db_name": "dev_portman",
            "db_user": "postgres",
            "db_password": "postgres",
            "function_auth_code": "dev_code",
            "log_level": "INFO"
        },
        "production": {
            "api_url": "https://meri.digitraffic.fi/api/port-call/v1",
            "db_host": "portman-db.postgres.database.azure.com",
            "db_port": "5432",
            "db_name": "portman",
            "db_user": "${DB_USER}",
            "db_password": "${DB_PASSWORD}",
            "function_auth_code": "${FUNCTION_CODE}",
            "log_level": "WARNING"
        }
    }

    # Get configuration for the specified environment
    config = configs.get(environment, configs["test"])

    # Replace environment variable placeholders
    for key, value in config.items():
        if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
            env_var = value[2:-1]
            config[key] = get_env_var(env_var, "")

    return config
