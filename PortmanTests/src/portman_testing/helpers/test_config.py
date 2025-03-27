# src/portman_testing/helpers/test_config.py

import os
from typing import Dict, Any


class PortmanTestEnvironment:
    """Test environment configuration manager."""

    def __init__(self, env_name: str = "test"):
        """Initialize with environment name."""
        self.env_name = env_name
        self.config = self._load_config(env_name)

    def _load_config(self, env_name: str) -> Dict[str, Any]:
        """Load configuration for the specified environment."""
        # Default configurations
        configs = {
            "test": {
                "db_host": "localhost",
                "db_port": "5432",
                "db_name": f"test_portman_{env_name}",
                "db_user": "postgres",
                "db_password": "postgres",
                "api_url": "https://meri.digitraffic.fi/api/port-call/v1"
            },
            "dev": {
                "db_host": "localhost",
                "db_port": "5432",
                "db_name": "dev_portman",
                "db_user": "postgres",
                "db_password": "postgres",
                "api_url": "https://meri.digitraffic.fi/api/port-call/v1"
            },
            "prod": {
                "db_host": os.environ.get("DB_HOST", "localhost"),
                "db_port": os.environ.get("DB_PORT", "5432"),
                "db_name": os.environ.get("DB_NAME", "portman"),
                "db_user": os.environ.get("DB_USER", "postgres"),
                "db_password": os.environ.get("DB_PASSWORD", "postgres"),
                "api_url": os.environ.get("API_URL", "https://meri.digitraffic.fi/api/port-call/v1")
            }
        }

        # Allow environment variable overrides for any config
        config = configs.get(env_name, configs["test"]).copy()
        for key in config:
            env_var = f"PORTMAN_TEST_{key.upper()}"
            if env_var in os.environ:
                config[key] = os.environ[env_var]

        return config

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)
