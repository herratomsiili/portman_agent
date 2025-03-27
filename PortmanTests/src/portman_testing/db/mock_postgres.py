"""
Database testing module for PostgreSQL.

This module provides tools for creating and managing test PostgreSQL databases
for testing the Portman Agent without affecting production databases.
"""

import os
import uuid
import psycopg2
from typing import Dict, List, Optional, Union, Any, Tuple
from contextlib import contextmanager

from .schema import (
    VOYAGES_TABLE_SQL,
    ARRIVALS_TABLE_SQL,
    get_test_data_sql
)


class MockPostgresDB:
    """
    Mock implementation of PostgreSQL database for testing.

    This class provides utilities for creating temporary test databases,
    executing queries, and managing test data for the Portman Agent.
    """

    def __init__(self,
                 dbname: str = "portman",
                 user: str = "postgres",
                 password: str = "postgres",
                 host: str = "localhost",
                 port: str = "5432"):
        """
        Initialize the MockPostgresDB instance.

        Args:
            dbname: Database name (default: "test_portman")
            user: Database user (default: "postgres")
            password: Database password (default: "postgres")
            host: Database host (default: "localhost")
            port: Database port (default: "5432")
        """
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.test_db_name = f"portman_{uuid.uuid4().hex[:8]}"
        self.conn = None

    def get_connection_string(self, database: Optional[str] = None) -> str:
        """
        Get the connection string for the database.

        Args:
            database: Database name (default: None, uses self.dbname)

        Returns:
            Connection string for psycopg2
        """
        db = database or self.dbname
        return f"dbname={db} user={self.user} password={self.password} host={self.host} port={self.port}"

    @contextmanager
    def get_connection(self, database: Optional[str] = None):
        """
        Context manager for database connections.

        Args:
            database: Database name (default: None, uses self.dbname)

        Yields:
            psycopg2 connection object
        """
        conn = None
        try:
            conn = psycopg2.connect(self.get_connection_string(database))
            yield conn
        finally:
            if conn:
                conn.close()

    def setup_test_db(self) -> str:
        """
        Create a temporary test database with the Portman Agent schema.

        Returns:
            Name of the created test database
        """
        # Connect to default PostgreSQL database to create test database
        with self.get_connection("postgres") as conn:
            conn.autocommit = True
            with conn.cursor() as cur:
                # Create test database
                cur.execute(f"DROP DATABASE IF EXISTS {self.test_db_name}")
                cur.execute(f"CREATE DATABASE {self.test_db_name}")

        # Connect to test database and create schema
        with self.get_connection(self.test_db_name) as conn:
            conn.autocommit = True
            with conn.cursor() as cur:
                # Create tables
                cur.execute(VOYAGES_TABLE_SQL)
                cur.execute(ARRIVALS_TABLE_SQL)

        return self.test_db_name

    def teardown_test_db(self) -> None:
        """
        Drop the temporary test database.
        """
        with self.get_connection("postgres") as conn:
            conn.autocommit = True
            with conn.cursor() as cur:
                # Terminate any connections to the test database
                cur.execute(f"""
                    SELECT pg_terminate_backend(pg_stat_activity.pid)
                    FROM pg_stat_activity
                    WHERE pg_stat_activity.datname = '{self.test_db_name}'
                    AND pid <> pg_backend_pid()
                """)
                # Drop test database
                cur.execute(f"DROP DATABASE IF EXISTS {self.test_db_name}")

    def execute_query(self, query: str, params: Optional[Tuple] = None,
                      database: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Execute a SQL query and return results as a list of dictionaries.

        Args:
            query: SQL query to execute
            params: Query parameters (default: None)
            database: Database name (default: None, uses test_db_name)

        Returns:
            List of dictionaries containing query results
        """
        db = database or self.test_db_name
        results = []

        with self.get_connection(db) as conn:
            with conn.cursor() as cur:
                cur.execute(query, params or ())

                # If query returns results
                if cur.description:
                    columns = [desc[0] for desc in cur.description]
                    for row in cur.fetchall():
                        results.append(dict(zip(columns, row)))

                conn.commit()

        return results

    def load_test_data(self, imo_numbers: Optional[List[str]] = None) -> None:
        """
        Load test data into the test database.

        Args:
            imo_numbers: List of IMO numbers to include in test data (default: None)
        """
        test_data_sql = get_test_data_sql(imo_numbers)

        with self.get_connection(self.test_db_name) as conn:
            conn.autocommit = True
            with conn.cursor() as cur:
                cur.execute(test_data_sql)

    def get_voyage_by_imo(self, imo: str) -> List[Dict[str, Any]]:
        """
        Get voyage data for a specific IMO number.

        Args:
            imo: IMO number to query

        Returns:
            List of dictionaries containing voyage data
        """
        query = "SELECT * FROM voyages WHERE vessel_imo = %s ORDER BY eta"
        return self.execute_query(query, (imo,))

    def get_arrivals_by_imo(self, imo: str) -> List[Dict[str, Any]]:
        """
        Get arrival data for a specific IMO number.

        Args:
            imo: IMO number to query

        Returns:
            List of dictionaries containing arrival data
        """
        query = "SELECT * FROM arrivals WHERE vessel_imo = %s ORDER BY timestamp"
        return self.execute_query(query, (imo,))

    def insert_voyage(self, voyage_data: Dict[str, Any]) -> None:
        """
        Insert a voyage record into the voyages table.

        Args:
            voyage_data: Dictionary containing voyage data
        """
        columns = ", ".join(voyage_data.keys())
        placeholders = ", ".join(["%s"] * len(voyage_data))
        values = tuple(voyage_data.values())

        query = f"INSERT INTO voyages ({columns}) VALUES ({placeholders})"
        self.execute_query(query, values)

    def insert_arrival(self, arrival_data: Dict[str, Any]) -> None:
        """
        Insert an arrival record into the arrivals table.

        Args:
            arrival_data: Dictionary containing arrival data
        """
        columns = ", ".join(arrival_data.keys())
        placeholders = ", ".join(["%s"] * len(arrival_data))
        values = tuple(arrival_data.values())

        query = f"INSERT INTO arrivals ({columns}) VALUES ({placeholders})"
        self.execute_query(query, values)
